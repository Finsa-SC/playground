import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Product, ProductModerationEvent, ProductStatus, ModerationAction, User
from app.db.session import get_session
from app.modules.auth.dependencies import require_role
from app.modules.catalog.service import product_payload

router = APIRouter(prefix="/moderation", tags=["Moderation"])


class RejectRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=2000)


@router.get("/products")
async def queue(
    operator: User = Depends(require_role("op")),
    session: AsyncSession = Depends(get_session),
):
    products = await session.scalars(
        select(Product).where(Product.status == ProductStatus.pending)
        .order_by(Product.submitted_at.asc()).limit(100)
    )
    return {"items": [product_payload(p) for p in products]}


@router.post("/products/{product_id}/approve")
async def approve(
    product_id: uuid.UUID,
    operator: User = Depends(require_role("op")),
    session: AsyncSession = Depends(get_session),
):
    product = await session.scalar(
        select(Product).where(Product.id == product_id).with_for_update()
    )
    if not product:
        raise HTTPException(404, "Product not found")
    if product.status != ProductStatus.pending:
        raise HTTPException(409, "Product is not pending moderation")
    now = datetime.now(timezone.utc)
    product.status = ProductStatus.approved
    product.approved_at = now
    product.approved_by = operator.id
    product.published_at = now
    session.add(ProductModerationEvent(
        product_id=product.id, moderator_id=operator.id,
        action=ModerationAction.approved, reason="Approved by operator",
    ))
    await session.commit()
    await session.refresh(product)
    return product_payload(product)


@router.post("/products/{product_id}/reject")
async def reject(
    product_id: uuid.UUID,
    payload: RejectRequest,
    operator: User = Depends(require_role("op")),
    session: AsyncSession = Depends(get_session),
):
    product = await session.scalar(
        select(Product).where(Product.id == product_id).with_for_update()
    )
    if not product:
        raise HTTPException(404, "Product not found")
    if product.status != ProductStatus.pending:
        raise HTTPException(409, "Product is not pending moderation")
    product.status = ProductStatus.rejected
    product.rejection_reason = payload.reason
    session.add(ProductModerationEvent(
        product_id=product.id, moderator_id=operator.id,
        action=ModerationAction.rejected, reason=payload.reason,
    ))
    await session.commit()
    await session.refresh(product)
    return product_payload(product)
