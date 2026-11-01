from fastapi import APIRouter
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.catalog.router import router as catalog_router
from app.modules.feed.router import router as feed_router
from app.modules.moderation.router import router as moderation_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(catalog_router)
api_router.include_router(feed_router)
api_router.include_router(moderation_router)
