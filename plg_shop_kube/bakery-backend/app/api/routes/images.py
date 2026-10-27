import io
import uuid
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.api.deps import require_roles
from app.core.config import settings
from app.db.session import get_db
from app.models.models import Product, ProductImage

router = APIRouter(prefix="/products", tags=["product images"])
ALLOWED_FORMATS = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}

@router.post("/{product_id}/images", status_code=201)
async def upload_product_image(product_id: int, file: UploadFile = File(...), alt_text: str | None = Form(default=None), is_primary: bool = Form(default=False), db: Session = Depends(get_db), _: object = Depends(require_roles("owner", "admin"))):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    max_bytes = settings.max_image_size_mb * 1024 * 1024
    content = await file.read(max_bytes + 1)
    if not content or len(content) > max_bytes:
        raise HTTPException(status_code=413, detail=f"Image must be smaller than {settings.max_image_size_mb} MB")
    try:
        image = Image.open(io.BytesIO(content))
        image.verify()
        image = Image.open(io.BytesIO(content))
        image_format = image.format
        width, height = image.size
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(status_code=415, detail="Uploaded file is not a valid supported image")
    if image_format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=415, detail="Only JPEG, PNG, and WEBP images are supported")
    if width > 8000 or height > 8000:
        raise HTTPException(status_code=400, detail="Image dimensions are too large")
    directory = Path(settings.image_storage_dir).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ALLOWED_FORMATS[image_format]}"
    destination = directory / filename
    destination.write_bytes(content)
    url = f"{settings.public_base_url.rstrip('/')}/media/product-images/{filename}"
    try:
        if is_primary:
            for old in product.images:
                old.is_primary = False
        record = ProductImage(product_id=product.id, url=url, alt_text=(alt_text or "")[:200] or None, is_primary=is_primary)
        db.add(record)
        db.commit()
        db.refresh(record)
    except Exception:
        db.rollback()
        destination.unlink(missing_ok=True)
        raise
    return {"id": record.id, "product_id": product.id, "url": record.url, "alt_text": record.alt_text, "is_primary": record.is_primary}

@router.delete("/{product_id}/images/{image_id}", status_code=204)
def delete_product_image(product_id: int, image_id: int, db: Session = Depends(get_db), _: object = Depends(require_roles("owner", "admin"))):
    record = db.get(ProductImage, image_id)
    if not record or record.product_id != product_id:
        raise HTTPException(status_code=404, detail="Product image not found")
    prefix = f"{settings.public_base_url.rstrip('/')}/media/product-images/"
    if record.url.startswith(prefix):
        filename = record.url.removeprefix(prefix)
        if Path(filename).name == filename:
            (Path(settings.image_storage_dir).resolve() / filename).unlink(missing_ok=True)
    db.delete(record)
    db.commit()
    return None
