from fastapi import APIRouter
from app.api.v1.endpoints import auth, comments, follows, health, media, posts, profiles
api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(profiles.router)
api_router.include_router(follows.router)
api_router.include_router(posts.router)
api_router.include_router(comments.router)
api_router.include_router(media.router)
