from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
router = APIRouter(tags=["health"])
@router.get("/health/live")
async def live(): return {"status": "ok"}
@router.get("/health/ready")
async def ready(db: AsyncSession = Depends(get_db_session)):
    await db.execute(text("SELECT 1"))
    return {"status": "ready", "database": "ok"}
