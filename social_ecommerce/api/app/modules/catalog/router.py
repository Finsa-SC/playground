import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.db.session import get_session
from app.modules.auth.dependencies import current_user, require_role
from app.modules.catalog import service
from app.modules.catalog.schemas import ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    payload: ProductCreate,
    seller: User = Depends(require_role("seller")),
    session: AsyncSession = Depends(get_session),
):
    try:
        product = await service.create_product(session, seller, payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return service.product_payload(product)


@router.get("/{product_id}")
async def get_one(
    product_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    # Public access is intentional; non-approved products are never disclosed here.
    product = await service.get_product_for_view(session, product_id, None)
    return service.product_payload(product)


@router.patch("/{product_id}")
async def update(
    product_id: uuid.UUID,
    payload: ProductUpdate,
    seller: User = Depends(require_role("seller")),
    session: AsyncSession = Depends(get_session),
):
    try:
        product = await service.update_product(
            session, product_id, seller, payload.model_dump(exclude_unset=True)
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return service.product_payload(product)


@router.post("/{product_id}/submit")
async def submit(
    product_id: uuid.UUID,
    seller: User = Depends(require_role("seller")),
    session: AsyncSession = Depends(get_session),
):
    try:
        product = await service.submit_product(session, product_id, seller)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return service.product_payload(product)
