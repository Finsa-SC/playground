from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db_session
from app.models import User, Profile
from app.schemas.auth import RegisterRequest, TokenOut, UserOut
router = APIRouter(prefix="/auth", tags=["authentication"])
@router.post("/register", response_model=UserOut, status_code=201)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db_session)):
    email = str(payload.email).lower()
    username = payload.username
    exists = await db.scalar(select(User.id).where((func.lower(User.email) == email) | (func.lower(User.username) == username.lower())))
    if exists:
        raise HTTPException(409, "Email or username already exists")
    user = User(email=email, username=username, password_hash=hash_password(payload.password))
    user.profile = Profile(display_name=payload.display_name)
    db.add(user)
    try:
        await db.commit()
        await db.refresh(user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(409, "Email or username already exists")
    return user
@router.post("/login", response_model=TokenOut)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db_session)):
    identifier = form.username.strip().lower()
    user = await db.scalar(select(User).where((func.lower(User.email) == identifier) | (func.lower(User.username) == identifier)))
    if user is None or not verify_password(form.password, user.password_hash) or not user.is_active:
        raise HTTPException(status_code=401, detail="Incorrect username/email or password", headers={"WWW-Authenticate":"Bearer"})
    return TokenOut(access_token=create_access_token(str(user.id)), expires_in=settings.access_token_expire_minutes * 60)
@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(get_current_user)): return user
