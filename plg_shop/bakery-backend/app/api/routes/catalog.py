from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.api.deps import require_roles
from app.db.session import get_db
from app.models.models import Category, Product
from app.schemas.products import CategoryCreate, CategoryOutput, ProductCreate, ProductUpdate, ProductOutput

router = APIRouter(tags=["catalog"])

def load_product_query():
    return select(Product).options(selectinload(Product.images))

@router.get("/categories", response_model=list[CategoryOutput])
def list_categories(db: Session = Depends(get_db)):
    return list(db.scalars(select(Category).order_by(Category.name)).all())

@router.post("/categories", response_model=CategoryOutput, status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), _: object = Depends(require_roles("owner", "admin"))):
    category = Category(name=payload.name.strip(), description=payload.description)
    db.add(category)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="Category name may already exist")
    db.refresh(category)
    return category

@router.get("/products", response_model=list[ProductOutput])
def list_products(search: str | None = None, category_id: int | None = None, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    query = load_product_query().where(Product.is_available.is_(True))
    if search:
        query = query.where(Product.name.ilike(f"%{search.strip()}%"))
    if category_id:
        query = query.where(Product.category_id == category_id)
    return list(db.scalars(query.order_by(Product.id).offset((page - 1) * page_size).limit(page_size)).all())

@router.get("/products/{product_id}", response_model=ProductOutput)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.scalar(load_product_query().where(Product.id == product_id, Product.is_available.is_(True)))
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products", response_model=ProductOutput, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db), _: object = Depends(require_roles("owner", "admin"))):
    if not db.get(Category, payload.category_id):
        raise HTTPException(status_code=400, detail="Category does not exist")
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return db.scalar(load_product_query().where(Product.id == product.id))

@router.patch("/products/{product_id}", response_model=ProductOutput)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db), _: object = Depends(require_roles("owner", "admin"))):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    changes = payload.model_dump(exclude_unset=True)
    if "category_id" in changes and changes["category_id"] is not None and not db.get(Category, changes["category_id"]):
        raise HTTPException(status_code=400, detail="Category does not exist")
    for key, value in changes.items():
        setattr(product, key, value)
    db.commit()
    return db.scalar(load_product_query().where(Product.id == product_id))

@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), _: object = Depends(require_roles("owner", "admin"))):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Soft-delete from the public catalog; preserve order history.
    product.is_available = False
    db.commit()
    return None
