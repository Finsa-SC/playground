import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import forbidden, not_found
from app.db.models import Category, Product, ProductStatus, User


async def create_product(session: AsyncSession, seller: User, data: dict) -> Product:
    category_id = data.get("category_id")
    if category_id:
        category = await session.get(Category, category_id)
        if not category or not category.is_active:
            raise ValueError("Category is unavailable")
    product = Product(
        id=uuid.uuid4(), seller_id=seller.id, status=ProductStatus.draft,
        **data,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def get_product_for_view(session: AsyncSession, product_id: uuid.UUID,
                               viewer: User | None) -> Product:
    product = await session.get(Product, product_id)
    if not product:
        raise not_found("Product not found")
    if product.status != ProductStatus.approved:
        if not viewer or (viewer.id != product.seller_id and not await is_operator(session, viewer.id)):
            raise not_found("Product not found")
    return product


async def is_operator(session: AsyncSession, user_id: uuid.UUID) -> bool:
    from app.db.models import Role, UserRole
    return bool(await session.scalar(
        select(UserRole.user_id).join(Role, Role.id == UserRole.role_id)
        .where(UserRole.user_id == user_id, Role.name == "op")
    ))


async def update_product(session: AsyncSession, product_id: uuid.UUID,
                         seller: User, data: dict) -> Product:
    product = await session.get(Product, product_id)
    if not product:
        raise not_found("Product not found")
    if product.seller_id != seller.id:
        raise forbidden()
    if product.status not in (ProductStatus.draft, ProductStatus.rejected):
        raise ValueError("Only draft or rejected products can be edited")
    for key, value in data.items():
        setattr(product, key, value)
    await session.commit()
    await session.refresh(product)
    return product


async def submit_product(session: AsyncSession, product_id: uuid.UUID, seller: User) -> Product:
    product = await session.get(Product, product_id)
    if not product:
        raise not_found("Product not found")
    if product.seller_id != seller.id:
        raise forbidden()
    if product.status not in (ProductStatus.draft, ProductStatus.rejected):
        raise ValueError("Product cannot be submitted in its current state")
    product.status = ProductStatus.pending
    product.submitted_at = datetime.now(timezone.utc)
    product.rejection_reason = None
    await session.commit()
    await session.refresh(product)
    return product


def product_payload(product: Product):
    return {
        "id": str(product.id), "seller_id": str(product.seller_id),
        "category_id": str(product.category_id) if product.category_id else None,
        "title": product.title, "description": product.description,
        "price": str(product.price), "currency": product.currency,
        "stock_quantity": product.stock_quantity, "status": product.status.value,
        "published_at": product.published_at,
        "created_at": product.created_at,
    }
