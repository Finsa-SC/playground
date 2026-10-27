from uuid import UUID
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.db.session import get_db_session
from app.models import User, Profile, Follow, Post
from app.schemas.profile import ProfileOut, ProfileUpdate
from app.services.media import save_upload, resolve_media_key
router = APIRouter(prefix="/profiles", tags=["profiles"])
async def load_profile(db: AsyncSession, user: User) -> Profile:
    profile = await db.get(Profile, user.id)
    if profile is None: raise HTTPException(404, "Profile not found")
    return profile
@router.get("/me", response_model=ProfileOut)
async def my_profile(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    return await load_profile(db, user)
@router.patch("/me", response_model=ProfileOut)
async def update_profile(payload: ProfileUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    profile = await load_profile(db, user)
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(profile, key, str(value) if key == "website_url" and value else value)
    await db.commit(); await db.refresh(profile); return profile
@router.get("/{username}")
async def public_profile(username: str, db: AsyncSession = Depends(get_db_session)):
    user = await db.scalar(select(User).where(func.lower(User.username) == username.lower(), User.is_active.is_(True)))
    if not user: raise HTTPException(404, "User not found")
    profile = await load_profile(db, user)
    followers = await db.scalar(select(func.count()).select_from(Follow).where(Follow.followed_id == user.id))
    following = await db.scalar(select(func.count()).select_from(Follow).where(Follow.follower_id == user.id))
    posts = await db.scalar(select(func.count()).select_from(Post).where(Post.author_id == user.id, Post.deleted_at.is_(None)))
    return {"user_id": str(user.id), "username": user.username, "profile": ProfileOut.model_validate(profile), "followers_count": followers or 0, "following_count": following or 0, "posts_count": posts or 0}
@router.post("/me/avatar", response_model=ProfileOut)
async def upload_avatar(file: UploadFile = File(...), user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    key, mime, size = await save_upload(file, "image", storage_folder="profiles/avatars")
    profile = await load_profile(db, user); profile.avatar_key = key
    await db.commit(); await db.refresh(profile)
    return profile
@router.post("/me/banner", response_model=ProfileOut)
async def upload_banner(file: UploadFile = File(...), user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    key, mime, size = await save_upload(file, "image", storage_folder="profiles/banners")
    profile = await load_profile(db, user); profile.banner_key = key
    await db.commit(); await db.refresh(profile)
    return profile

@router.get("/{username}/avatar")
async def get_avatar(username: str, db: AsyncSession = Depends(get_db_session)):
    user = await db.scalar(select(User).where(func.lower(User.username) == username.lower(), User.is_active.is_(True)))
    if not user: raise HTTPException(404, "User not found")
    profile = await load_profile(db, user)
    if not profile.avatar_key: raise HTTPException(404, "Avatar not found")
    path = resolve_media_key(profile.avatar_key)
    if not path.is_file(): raise HTTPException(404, "Avatar file not found")
    return FileResponse(path)
@router.get("/{username}/banner")
async def get_banner(username: str, db: AsyncSession = Depends(get_db_session)):
    user = await db.scalar(select(User).where(func.lower(User.username) == username.lower(), User.is_active.is_(True)))
    if not user: raise HTTPException(404, "User not found")
    profile = await load_profile(db, user)
    if not profile.banner_key: raise HTTPException(404, "Banner not found")
    path = resolve_media_key(profile.banner_key)
    if not path.is_file(): raise HTTPException(404, "Banner file not found")
    return FileResponse(path)
