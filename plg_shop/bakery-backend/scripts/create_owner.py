"""Create the first owner account from environment variables."""
import os
from sqlalchemy import select
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.models import User

email = os.environ.get("OWNER_EMAIL", "").strip().lower()
name = os.environ.get("OWNER_NAME", "Bakery Owner").strip()
password = os.environ.get("OWNER_PASSWORD", "")
if not email or not password:
    raise SystemExit("Set OWNER_EMAIL and OWNER_PASSWORD before running this script.")
if len(password) < 12:
    raise SystemExit("OWNER_PASSWORD must contain at least 12 characters.")
with SessionLocal() as db:
    if db.scalar(select(User).where(User.email == email)):
        raise SystemExit("A user with this email already exists.")
    db.add(User(email=email, full_name=name, password_hash=hash_password(password), role="owner"))
    db.commit()
print(f"Owner account created for {email}")
