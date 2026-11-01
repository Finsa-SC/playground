from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.modules.auth import service
from app.modules.auth.dependencies import current_user
from app.modules.auth.schemas import RegisterRequest, LoginRequest, TokenResponse
from app.db.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_session)):
    try:
        user = await service.register(session, **payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return {"id": str(user.id), "username": user.username, "email": user.email}


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)):
    user = await service.authenticate(session, payload.email, payload.password)
    return await service.issue_tokens(session, user)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_token: str, session: AsyncSession = Depends(get_session)):
    return await service.rotate_refresh(session, refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    refresh_token: str,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_session),
):
    await service.revoke_refresh(session, user.id, refresh_token)
    return None
