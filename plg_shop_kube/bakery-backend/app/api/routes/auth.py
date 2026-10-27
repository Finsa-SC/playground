from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token, new_refresh_token, hash_token
from app.db.session import get_db
from app.models.models import User, RefreshToken
from app.schemas.auth import RegisterInput, LoginInput, RefreshInput, TokenOutput, UserOutput

router = APIRouter(prefix="/auth", tags=["authentication"])

def issue_tokens(db: Session, user: User) -> TokenOutput:
    refresh = new_refresh_token()
    db.add(RefreshToken(user_id=user.id, token_hash=hash_token(refresh), expires_at=datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days)))
    db.commit()
    return TokenOutput(access_token=create_access_token(user.id, user.role), expires_in=settings.access_token_minutes * 60, refresh_token=refresh, user=user)

@router.post("/register", response_model=UserOutput, status_code=201)
def register(payload: RegisterInput, db: Session = Depends(get_db)):
    email = str(payload.email).lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = User(email=email, full_name=payload.full_name.strip(), password_hash=hash_password(payload.password), role="customer")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenOutput)
def login(payload: LoginInput, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if not user or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    return issue_tokens(db, user)

@router.post("/refresh", response_model=TokenOutput)
def refresh(payload: RefreshInput, db: Session = Depends(get_db)):
    stored = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_token(payload.refresh_token)))
    now = datetime.now(timezone.utc)
    if not stored or stored.revoked_at is not None or stored.expires_at <= now:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    user = db.get(User, stored.user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User is unavailable")
    stored.revoked_at = now
    db.commit()
    return issue_tokens(db, user)

@router.post("/logout", status_code=204)
def logout(payload: RefreshInput, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    stored = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_token(payload.refresh_token), RefreshToken.user_id == user.id))
    if stored and stored.revoked_at is None:
        stored.revoked_at = datetime.now(timezone.utc)
        db.commit()
    return None

@router.get("/me", response_model=UserOutput)
def me(user: User = Depends(get_current_user)):
    return user
