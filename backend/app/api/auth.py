import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.base import get_db
from app.db.models import User
from app.schemas.user import LoginIn, RegisterIn, TokenOut, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])

GUEST_AVATARS = ["🧑🏻", "👩🏽", "👨🏿", "🧔🏻", "👩🏻‍🦱", "👨🏽‍🦰"]


@router.post("/register", response_model=TokenOut, status_code=201)
def register(body: RegisterIn, db: Session = Depends(get_db)) -> TokenOut:
    exists = db.scalar(select(User).where(User.username == body.username))
    if exists:
        raise HTTPException(status_code=409, detail={"code": "username_taken", "message": "Username is already taken"})
    if body.email and db.scalar(select(User).where(User.email == body.email)):
        raise HTTPException(status_code=409, detail={"code": "email_taken", "message": "Email is already registered"})
    user = User(username=body.username, email=body.email, password_hash=hash_password(body.password))
    db.add(user)
    db.commit()
    return TokenOut(access_token=create_access_token(str(user.id)))


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)) -> TokenOut:
    user = db.scalar(select(User).where(User.username == body.username))
    if user is None or user.password_hash is None or not verify_password(body.password, user.password_hash):
        # Generic error: do not reveal which part failed (PRD FR-AUTH-02).
        raise HTTPException(status_code=401, detail={"code": "invalid_credentials", "message": "Invalid username or password"})
    return TokenOut(access_token=create_access_token(str(user.id)))


@router.post("/guest", response_model=TokenOut, status_code=201)
def guest(db: Session = Depends(get_db)) -> TokenOut:
    suffix = secrets.token_hex(3)
    user = User(
        username=f"guest_{suffix}",
        is_guest=True,
        avatar=secrets.choice(GUEST_AVATARS),
    )
    db.add(user)
    db.commit()
    return TokenOut(access_token=create_access_token(str(user.id), extra={"guest": True}))


@router.post("/refresh", response_model=TokenOut)
def refresh(user: User = Depends(get_current_user)) -> TokenOut:
    extra = {"guest": True} if user.is_guest else None
    return TokenOut(access_token=create_access_token(str(user.id), extra=extra))


users_router = APIRouter(prefix="/api/users", tags=["users"])


@users_router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(user)
