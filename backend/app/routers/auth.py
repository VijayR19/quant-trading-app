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
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user