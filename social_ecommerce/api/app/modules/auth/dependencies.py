import uuid
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import unauthorized, forbidden
from app.core.security import decode_access_token
from app.db.models import Role, User, UserRole
from app.db.session import get_session

bearer = HTTPBearer(auto_error=False)


async def current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    session: AsyncSession = Depends(get_session),
) -> User:
    if credentials is None:
        raise unauthorized()
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = uuid.UUID(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise unauthorized("Invalid access token")
    user = await session.get(User, user_id)
    if not user or user.deleted_at is not None or user.status.value != "active":
        raise unauthorized("Account is unavailable")
    return user


def require_role(role_name: str):
    async def dependency(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_session),
    ) -> User:
        found = await session.scalar(
            select(UserRole.user_id)
            .join(Role, Role.id == UserRole.role_id)
            .where(UserRole.user_id == user.id, Role.name == role_name)
        )
        if not found:
            raise forbidden(f"Role '{role_name}' required")
        return user
    return dependency
