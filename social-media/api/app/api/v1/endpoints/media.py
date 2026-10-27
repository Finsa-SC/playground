from pathlib import Path
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from sqlalchemy import select
import jwt
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.db.session import get_db_session
from app.models import User, PostMedia, Post, Profile
from app.api.v1.endpoints.posts import can_view
from app.services.media import resolve_media_key
router = APIRouter(prefix="/media", tags=["media"])
async def optional_media_user(token: str | None = Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)), db: AsyncSession = Depends(get_db_session)):
    if not token: return None
    try: user_id = UUID(decode_access_token(token)["sub"])
    except Exception: return None
    user = await db.get(User, user_id)
    return user if user and user.is_active else None
@router.get("/{media_id}")
async def get_media(media_id: UUID, user: User | None = Depends(optional_media_user), db: AsyncSession = Depends(get_db_session)):
    media = await db.get(PostMedia, media_id)
    if not media: raise HTTPException(404, "Media not found")
    post = await db.get(Post, media.post_id)
    if not post or post.deleted_at or not await can_view(post, user, db): raise HTTPException(404, "Media not found")
    path = resolve_media_key(media.media_url)
    if not path.is_file(): raise HTTPException(404, "Media file not found")
    return FileResponse(path, media_type=media.mime_type or "application/octet-stream", filename=path.name)
