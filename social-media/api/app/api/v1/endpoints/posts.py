from datetime import datetime, timezone
from uuid import UUID
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select, func, exists, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, oauth2_scheme
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
import jwt
from uuid import UUID as UUIDType
from app.db.session import get_db_session
from app.models import User, Post, PostMedia, PostLike, Follow, Comment
from app.schemas.post import PostCreate, PostUpdate, PostOut, MediaOut
from app.services.media import save_upload
router = APIRouter(tags=["posts"])
async def optional_user(token: str | None = Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)), db: AsyncSession = Depends(get_db_session)) -> User | None:
    if not token: return None
    try:
        payload = decode_access_token(token); user_id = UUID(payload["sub"])
    except Exception: return None
    user = await db.get(User, user_id)
    return user if user and user.is_active else None
async def can_view(post: Post, viewer: User | None, db: AsyncSession) -> bool:
    if post.visibility == "public" or (viewer and viewer.id == post.author_id): return True
    if viewer is None: return False
    return await db.scalar(select(exists().where(Follow.follower_id == viewer.id, Follow.followed_id == post.author_id))) or False
async def serialize_post(post: Post, db: AsyncSession, viewer: User | None):
    media = (await db.scalars(select(PostMedia).where(PostMedia.post_id == post.id).order_by(PostMedia.position))).all()
    likes = await db.scalar(select(func.count()).select_from(PostLike).where(PostLike.post_id == post.id))
    comments = await db.scalar(select(func.count()).select_from(Comment).where(Comment.post_id == post.id, Comment.deleted_at.is_(None)))
    liked = bool(viewer and await db.get(PostLike, (viewer.id, post.id)))
    return PostOut(id=post.id, author_id=post.author_id, content=post.content, visibility=post.visibility, created_at=post.created_at, updated_at=post.updated_at, edited_at=post.edited_at, like_count=likes or 0, comment_count=comments or 0, liked_by_me=liked, media=[MediaOut.model_validate(m) for m in media])
@router.post("/posts", response_model=PostOut, status_code=201)
async def create_post(payload: PostCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    post = Post(author_id=user.id, content=payload.content.strip() if payload.content else None, visibility=payload.visibility)
    db.add(post); await db.flush(); await db.commit(); await db.refresh(post)
    return await serialize_post(post, db, user)
@router.get("/posts/{post_id}", response_model=PostOut)
async def get_post(post_id: UUID, user: User | None = Depends(optional_user), db: AsyncSession = Depends(get_db_session)):
    post = await db.get(Post, post_id)
    if not post or post.deleted_at: raise HTTPException(404, "Post not found")
    if not await can_view(post, user, db): raise HTTPException(404, "Post not found")
    return await serialize_post(post, db, user)

@router.patch("/posts/{post_id}", response_model=PostOut)
async def update_post(post_id: UUID, payload: PostUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    post = await db.get(Post, post_id)
    if not post or post.deleted_at: raise HTTPException(404, "Post not found")
    if post.author_id != user.id: raise HTTPException(403, "You can only edit your own posts")
    changes = payload.model_dump(exclude_unset=True)
    if "content" in changes: post.content = changes["content"].strip() if changes["content"] else None
    if "visibility" in changes: post.visibility = changes["visibility"]
    post.edited_at = datetime.now(timezone.utc); await db.commit(); await db.refresh(post)
    return await serialize_post(post, db, user)
@router.delete("/posts/{post_id}", status_code=204)
async def delete_post(post_id: UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    post = await db.get(Post, post_id)
    if not post or post.deleted_at: raise HTTPException(404, "Post not found")
    if post.author_id != user.id: raise HTTPException(403, "You can only delete your own posts")
    post.deleted_at = datetime.now(timezone.utc); await db.commit()
@router.get("/feed/foryou", response_model=list[PostOut])
async def feed_foryou(limit: int = 20, offset: int = 0, user: User | None = Depends(optional_user), db: AsyncSession = Depends(get_db_session)):
    stmt = select(Post).where(Post.deleted_at.is_(None), Post.visibility == "public").order_by(Post.created_at.desc()).limit(min(max(limit,1),50)).offset(max(offset,0))
    posts = (await db.scalars(stmt)).all()
    return [await serialize_post(p, db, user) for p in posts]
@router.get("/feed/following", response_model=list[PostOut])
async def feed_following(limit: int = 20, offset: int = 0, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    ids = select(Follow.followed_id).where(Follow.follower_id == user.id)
    stmt = select(Post).where(Post.deleted_at.is_(None), ((Post.author_id.in_(ids)) | (Post.author_id == user.id)), Post.visibility.in_(["public", "followers"])).order_by(Post.created_at.desc()).limit(min(max(limit,1),50)).offset(max(offset,0))
    posts = (await db.scalars(stmt)).all()
    result=[]
    for p in posts:
        if await can_view(p, user, db): result.append(await serialize_post(p, db, user))
    return result
@router.get("/users/{user_id}/posts", response_model=list[PostOut])
async def user_posts(user_id: UUID, limit: int = 20, offset: int = 0, viewer: User | None = Depends(optional_user), db: AsyncSession = Depends(get_db_session)):
    if not await db.get(User, user_id): raise HTTPException(404, "User not found")
    posts = (await db.scalars(select(Post).where(Post.author_id == user_id, Post.deleted_at.is_(None)).order_by(Post.created_at.desc()).limit(min(max(limit,1),50)).offset(max(offset,0)))).all()
    result=[]
    for p in posts:
        if await can_view(p, viewer, db): result.append(await serialize_post(p, db, viewer))
    return result
@router.post("/posts/{post_id}/media", response_model=MediaOut, status_code=201)
async def upload_post_media(post_id: UUID, file: UploadFile = File(...), media_type: str = Form(...), alt_text: str | None = Form(default=None), user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    post = await db.get(Post, post_id)
    if not post or post.deleted_at: raise HTTPException(404, "Post not found")
    if post.author_id != user.id: raise HTTPException(403, "You can only add media to your own posts")
    if media_type not in {"image", "video"}: raise HTTPException(422, "media_type must be image or video")
    count = await db.scalar(select(func.count()).select_from(PostMedia).where(PostMedia.post_id == post_id))
    if count >= 4: raise HTTPException(400, "A post can contain at most 4 media files")
    key, mime, size = await save_upload(file, media_type)
    media = PostMedia(post_id=post_id, media_type=media_type, storage_key=key, alt_text=alt_text, mime_type=mime, file_size_bytes=size, position=count or 0)
    db.add(media)
    try: await db.commit(); await db.refresh(media)
    except Exception:
        await db.rollback()
        from pathlib import Path
        from app.services.media import resolve_media_key
        resolve_media_key(key).unlink(missing_ok=True)
        raise
    return media
@router.post("/posts/{post_id}/like", status_code=204)
async def like_post(post_id: UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    post = await db.get(Post, post_id)
    if not post or post.deleted_at or not await can_view(post, user, db): raise HTTPException(404, "Post not found")
    if await db.get(PostLike, (user.id, post_id)) is None: db.add(PostLike(user_id=user.id, post_id=post_id)); await db.commit()
@router.delete("/posts/{post_id}/like", status_code=204)
async def unlike_post(post_id: UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    await db.execute(delete(PostLike).where(PostLike.user_id == user.id, PostLike.post_id == post_id)); await db.commit()
