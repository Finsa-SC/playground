from datetime import datetime, timezone
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.db.session import get_db_session
from app.models import User, Post, Comment, Follow
from app.schemas.comment import CommentCreate, CommentUpdate, CommentOut
from app.api.v1.endpoints.posts import can_view
router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])
@router.get("", response_model=list[CommentOut])
async def list_comments(post_id: UUID, limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db_session)):
    post = await db.get(Post, post_id)
    if not post or post.deleted_at or post.visibility != "public": raise HTTPException(404, "Post not found")
    rows = (await db.scalars(select(Comment).where(Comment.post_id == post_id, Comment.deleted_at.is_(None)).order_by(Comment.created_at.asc()).limit(min(max(limit,1),100)).offset(max(offset,0)))).all()
    return rows
@router.post("", response_model=CommentOut, status_code=201)
async def create_comment(post_id: UUID, payload: CommentCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    post = await db.get(Post, post_id)
    if not post or post.deleted_at or not await can_view(post, user, db): raise HTTPException(404, "Post not found")
    content = payload.content.strip()
    if not content: raise HTTPException(422, "Comment cannot be blank")
    if payload.parent_comment_id:
        parent = await db.get(Comment, payload.parent_comment_id)
        if not parent or parent.post_id != post_id or parent.deleted_at: raise HTTPException(422, "Invalid parent comment")
    comment = Comment(post_id=post_id, author_id=user.id, parent_comment_id=payload.parent_comment_id, content=content)
    db.add(comment); await db.commit(); await db.refresh(comment); return comment
@router.patch("/{comment_id}", response_model=CommentOut)
async def update_comment(post_id: UUID, comment_id: UUID, payload: CommentUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    comment = await db.get(Comment, comment_id)
    if not comment or comment.post_id != post_id or comment.deleted_at: raise HTTPException(404, "Comment not found")
    if comment.author_id != user.id: raise HTTPException(403, "You can only edit your own comments")
    if not payload.content.strip(): raise HTTPException(422, "Comment cannot be blank")
    comment.content=payload.content.strip(); comment.edited_at=datetime.now(timezone.utc)
    await db.commit(); await db.refresh(comment); return comment
@router.delete("/{comment_id}", status_code=204)
async def delete_comment(post_id: UUID, comment_id: UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    comment = await db.get(Comment, comment_id)
    if not comment or comment.post_id != post_id or comment.deleted_at: raise HTTPException(404, "Comment not found")
    if comment.author_id != user.id: raise HTTPException(403, "You can only delete your own comments")
    comment.deleted_at=datetime.now(timezone.utc); await db.commit()
