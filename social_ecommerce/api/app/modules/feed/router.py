from fastapi import APIRouter, Query
from sqlalchemy import select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.models import Product, ProductStatus, User
from app.db.session import get_session
from app.modules.catalog.service import product_payload

router = APIRouter(prefix="/feed", tags=["Feed"])


@router.get("")
async def feed(
    limit: int = Query(default=20, ge=1, le=50),
    cursor_published_at: str | None = None,
    cursor_id: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Product).where(Product.status == ProductStatus.approved)
    if cursor_published_at and cursor_id:
        from datetime import datetime
        import uuid
        stmt = stmt.where(tuple_(Product.published_at, Product.id) <
                          tuple_(datetime.fromisoformat(cursor_published_at), uuid.UUID(cursor_id)))
    stmt = stmt.order_by(Product.published_at.desc(), Product.id.desc()).limit(limit + 1)
    products = list((await session.scalars(stmt)).all())
    has_more = len(products) > limit
    products = products[:limit]
    next_cursor = None
    if has_more and products:
        last = products[-1]
        next_cursor = {
            "published_at": last.published_at.isoformat(),
            "id": str(last.id),
        }
    return {"items": [product_payload(p) for p in products],
            "next_cursor": next_cursor}
