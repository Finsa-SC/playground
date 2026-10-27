
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import auth, catalog, images, orders
from app.core.config import settings

# Create the directory before StaticFiles checks it.
image_storage_path = Path(settings.image_storage_dir)
image_storage_path.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Schema changes should be applied with Alembic migrations.
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.mount(
    "/media/product-images",
    StaticFiles(directory=str(image_storage_path)),
    name="product-images",
)

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(catalog.router, prefix=settings.api_v1_prefix)
app.include_router(images.router, prefix=settings.api_v1_prefix)
app.include_router(orders.router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["operations"])
def health():
    return {"status": "ok"}
