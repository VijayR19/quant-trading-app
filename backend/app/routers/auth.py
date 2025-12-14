from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models import User
from app.schemas import UserCreate, TokenPair, LoginRequest, UserRead
from app.core.security import hash_password, verify_password, create_token
from app.core.config import settings


router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        payload (UserCreate): The user to be registered.
        db (Session): The database session.

    Returns:
        UserRead: The registered user.

    Raises:
        HTTPException: If the email is already registered.
    """
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=TokenPair)
def login_credentials(db: Session = Depends(get_db), credentials: LoginRequest):
    """
    Authenticate a user and return access and refresh tokens.

    Args:
        db (Session): The database session.
        credentials (LoginRequest): The login request containing email and password.

    Returns:
        TokenPair: The access and refresh tokens.

    Raises:
        HTTPException: If the email is not found or the password is incorrect.
    """
    user = db.query(User).filter_by(email=credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token_expires_delta = timedelta(minutes=settings.access_token_minutes)
    refresh_token_expires_delta = timedelta(days=settings.refresh_token_days)

    access_token = create_token(
        subject=str(user.id),
        token_type="access",
        expires_delta=access_token_expires_delta
    )
    refresh_token = create_token(
        subject=str(user.id),
        token_type="refresh",
        expires_delta=refresh_token_expires_delta
    )
    return TokenPair(access_token=access_token, refresh_token=refresh_token)
