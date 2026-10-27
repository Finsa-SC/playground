from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import engine
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.media_root.mkdir(parents=True, exist_ok=True)
    yield
    await engine.dispose()
app = FastAPI(title=settings.app_name, version="0.1.0", docs_url="/docs" if settings.environment != "production" else None, redoc_url=None, lifespan=lifespan)
if settings.cors_origins:
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["GET","POST","PATCH","DELETE","OPTIONS"], allow_headers=["Authorization","Content-Type"])
app.include_router(api_router, prefix=settings.api_v1_prefix)
@app.get("/", include_in_schema=False)
async def root(): return {"name": settings.app_name, "docs": "/docs" if settings.environment != "production" else None}
