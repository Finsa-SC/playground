from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.db.session import get_db_session
from app.models import User, Follow
router = APIRouter(prefix="/users", tags=["follows"])
@router.post("/{user_id}/follow", status_code=204)
async def follow_user(user_id: UUID, current: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    if user_id == current.id: raise HTTPException(400, "You cannot follow yourself")
    target = await db.get(User, user_id)
    if target is None or not target.is_active: raise HTTPException(404, "User not found")
    if await db.get(Follow, (current.id, user_id)) is None:
        db.add(Follow(follower_id=current.id, followed_id=user_id)); await db.commit()
@router.delete("/{user_id}/follow", status_code=204)
async def unfollow_user(user_id: UUID, current: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    await db.execute(delete(Follow).where(Follow.follower_id == current.id, Follow.followed_id == user_id)); await db.commit()
@router.get("/{user_id}/followers")
async def followers(user_id: UUID, limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db_session)):
    if not await db.get(User, user_id): raise HTTPException(404, "User not found")
    rows = (await db.execute(select(User.id, User.username).join(Follow, Follow.follower_id == User.id).where(Follow.followed_id == user_id).order_by(Follow.created_at.desc()).limit(min(max(limit,1),100)).offset(max(offset,0)))).all()
    return [{"id":str(r.id),"username":r.username} for r in rows]
@router.get("/{user_id}/following")
async def following(user_id: UUID, limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db_session)):
    if not await db.get(User, user_id): raise HTTPException(404, "User not found")
    rows = (await db.execute(select(User.id, User.username).join(Follow, Follow.followed_id == User.id).where(Follow.follower_id == user_id).order_by(Follow.created_at.desc()).limit(min(max(limit,1),100)).offset(max(offset,0)))).all()
    return [{"id":str(r.id),"username":r.username} for r in rows]
