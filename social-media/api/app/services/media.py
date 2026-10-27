from pathlib import Path, PurePosixPath
from uuid import uuid4
import mimetypes
from fastapi import HTTPException, UploadFile, status
from app.core.config import settings

IMAGE_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}
VIDEO_TYPES = {"video/mp4": ".mp4", "video/webm": ".webm", "video/quicktime": ".mov"}

def resolve_media_key(key: str) -> Path:
    # Treat DB values as relative POSIX storage keys, never arbitrary paths.
    p = PurePosixPath(key)
    if p.is_absolute() or ".." in p.parts or not p.parts:
        raise HTTPException(status_code=404, detail="Media not found")
    root = settings.media_root.resolve()
    target = (root / Path(*p.parts)).resolve()
    if root not in target.parents:
        raise HTTPException(status_code=404, detail="Media not found")
    return target

async def save_upload(upload: UploadFile, kind: str, *, storage_folder: str | None = None) -> tuple[str, str, int]:
    allowed = IMAGE_TYPES if kind == "image" else VIDEO_TYPES
    mime = (upload.content_type or "").lower()
    if mime not in allowed:
        raise HTTPException(status_code=415, detail=f"Unsupported {kind} content type")
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    data = await upload.read(max_bytes + 1)
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")
    if len(data) > max_bytes:
        raise HTTPException(status_code=413, detail="File exceeds upload size limit")
    # Basic signature checks; MIME headers alone are not trusted.
    valid = True
    if mime == "image/jpeg": valid = data.startswith(b"\xff\xd8\xff")
    elif mime == "image/png": valid = data.startswith(b"\x89PNG\r\n\x1a\n")
    elif mime == "image/webp": valid = len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    elif mime == "image/gif": valid = data.startswith((b"GIF87a", b"GIF89a"))
    elif mime == "video/mp4": valid = len(data) >= 12 and data[4:8] == b"ftyp"
    elif mime == "video/webm": valid = data.startswith(b"\x1aE\xdf\xa3")
    if not valid:
        raise HTTPException(status_code=415, detail="File signature does not match content type")
    folder = storage_folder or ("posts/images" if kind == "image" else "posts/videos")
    suffix = allowed[mime]
    key = f"{folder}/{uuid4().hex}{suffix}"
    path = resolve_media_key(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return key, mime, len(data)
