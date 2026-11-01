from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import not_found
from app.db.models import User
from app.db.session import get_session
from app.modules.auth.dependencies import current_user
from app.modules.users.schemas import ProfileUpdate

router = APIRouter(prefix="/users", tags=["Users"])


def profile_payload(user: User):
    return {
        "id": str(user.id), "username": user.username,
        "display_name": user.display_name, "bio": user.bio,
        "avatar_key": user.avatar_key, "banner_key": user.banner_key,
    }


@router.get("/me")
async def me(user: User = Depends(current_user)):
    return profile_payload(user)


@router.patch("/me")
async def update_me(
    payload: ProfileUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_session),
):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return profile_payload(user)


@router.get("/{username}")
async def public_profile(username: str, session: AsyncSession = Depends(get_session)):
    user = await session.scalar(
        select(User).where(User.username == username, User.deleted_at.is_(None))
    )
    if not user:
        raise not_found("User not found")
    return profile_payload(user)
