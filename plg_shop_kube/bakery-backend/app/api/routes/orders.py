from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.models import Order, OrderItem, Product, User
from app.schemas.orders import OrderCreate, OrderOutput, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["orders"])

def order_query():
    return select(Order).options(selectinload(Order.items))

@router.post("", response_model=OrderOutput, status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Aggregate duplicate product IDs so each product appears once per order.
    quantities: dict[int, int] = {}
    for item in payload.items:
        quantities[item.product_id] = quantities.get(item.product_id, 0) + item.quantity
    if any(quantity > 1000 for quantity in quantities.values()):
        raise HTTPException(status_code=422, detail="Requested quantity is too large")
    try:
        total = Decimal("0.00")
        items: list[OrderItem] = []
        # Lock product rows to reduce overselling when orders are placed concurrently.
        products = {}
        for product_id in sorted(quantities):
            product = db.scalar(select(Product).where(Product.id == product_id).with_for_update())
            if not product or not product.is_available:
                raise HTTPException(status_code=400, detail=f"Product {product_id} is unavailable")
            if product.stock_quantity < quantities[product_id]:
                raise HTTPException(status_code=409, detail=f"Insufficient stock for product {product_id}")
            products[product_id] = product
        for product_id, quantity in quantities.items():
            product = products[product_id]
            product.stock_quantity -= quantity
            line_total = product.price * quantity
            total += line_total
            items.append(OrderItem(product_id=product_id, quantity=quantity, unit_price=product.price))
        order = Order(customer_id=user.id, total_amount=total, status="pending", items=items)
        db.add(order)
        db.commit()
        return db.scalar(order_query().where(Order.id == order.id))
    except Exception:
        db.rollback()
        raise

@router.get("/mine", response_model=list[OrderOutput])
def list_my_orders(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return list(db.scalars(order_query().where(Order.customer_id == user.id).order_by(Order.created_at.desc())).all())

@router.get("", response_model=list[OrderOutput])
def list_all_orders(page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100), db: Session = Depends(get_db), _: User = Depends(require_roles("owner", "admin"))):
    return list(db.scalars(order_query().order_by(Order.created_at.desc()).offset((page - 1) * page_size).limit(page_size)).all())

@router.patch("/{order_id}", response_model=OrderOutput)
def update_order_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles("owner", "admin"))):
    order = db.scalar(order_query().where(Order.id == order_id).with_for_update())
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status in {"completed", "cancelled"}:
        raise HTTPException(status_code=409, detail="A completed or cancelled order cannot be changed")
    if payload.status == "cancelled":
        # Restore stock only when cancelling an order that has not already been cancelled.
        for item in order.items:
            product = db.scalar(select(Product).where(Product.id == item.product_id).with_for_update())
            if product:
                product.stock_quantity += item.quantity
    order.status = payload.status
    db.commit()
    return db.scalar(order_query().where(Order.id == order_id))
