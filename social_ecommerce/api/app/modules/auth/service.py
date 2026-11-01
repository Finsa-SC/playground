import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.core.errors import unauthorized
from app.core.security import (
    create_access_token, hash_password, new_refresh_token, token_digest, verify_password
)
from app.db.models import AuthSession, Role, User, UserRole, UserStatus

settings = get_settings()


async def register(session: AsyncSession, *, email: str, username: str,
                   display_name: str, password: str) -> User:
    existing = await session.scalar(
        select(User.id).where((User.email == email) | (User.username == username))
    )
    if existing:
        raise ValueError("Email or username is already registered")

    buyer_role = await session.scalar(select(Role).where(Role.name == "buyer"))
    if buyer_role is None:
        raise RuntimeError("Required role 'buyer' is missing; run database seeds first")

    user = User(
        id=uuid.uuid4(), email=email, username=username, display_name=display_name,
        password_hash=hash_password(password), status=UserStatus.active,
    )
    session.add(user)
    await session.flush()
    session.add(UserRole(user_id=user.id, role_id=buyer_role.id))
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate(session: AsyncSession, email: str, password: str) -> User:
    user = await session.scalar(select(User).where(User.email == email, User.deleted_at.is_(None)))
    if not user or not user.password_hash or not verify_password(password, user.password_hash):
        raise unauthorized("Invalid email or password")
    if user.status != UserStatus.active:
        raise unauthorized("Account is not active")
    return user


async def issue_tokens(session: AsyncSession, user: User) -> dict:
    refresh = new_refresh_token()
    now = datetime.now(timezone.utc)
    session.add(AuthSession(
        user_id=user.id,
        token_hash=token_digest(refresh),
        expires_at=now + timedelta(days=settings.refresh_token_days),
    ))
    await session.commit()
    return {
        "access_token": create_access_token(str(user.id)),
        "refresh_token": refresh,
        "token_type": "bearer",
        "expires_in": settings.access_token_minutes * 60,
    }


async def rotate_refresh(session: AsyncSession, raw_token: str) -> dict:
    digest = token_digest(raw_token)
    now = datetime.now(timezone.utc)
    record = await session.scalar(
        select(AuthSession).where(
            AuthSession.token_hash == digest,
            AuthSession.revoked_at.is_(None),
            AuthSession.expires_at > now,
        ).with_for_update()
    )
    if not record:
        raise unauthorized("Invalid or expired refresh token")

    # Revoke old token and issue a new one in the same DB transaction.
    record.revoked_at = now
    user = await session.get(User, record.user_id)
    if not user or user.status != UserStatus.active:
        await session.rollback()
        raise unauthorized("Account is not active")

    replacement = new_refresh_token()
    session.add(AuthSession(
        user_id=user.id,
        token_hash=token_digest(replacement),
        expires_at=now + timedelta(days=settings.refresh_token_days),
    ))
    await session.commit()
    return {
        "access_token": create_access_token(str(user.id)),
        "refresh_token": replacement,
        "token_type": "bearer",
        "expires_in": settings.access_token_minutes * 60,
    }


async def revoke_refresh(session: AsyncSession, user_id: uuid.UUID, raw_token: str) -> None:
    await session.execute(
        update(AuthSession)
        .where(
            AuthSession.user_id == user_id,
            AuthSession.token_hash == token_digest(raw_token),
            AuthSession.revoked_at.is_(None),
        )
        .values(revoked_at=datetime.now(timezone.utc))
    )
    await session.commit()
