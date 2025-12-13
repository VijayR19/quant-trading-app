from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models import User
from app.schemas import UserCreate, TokenPair, LoginRequest, UserRead
from app.core.security import hash_password, verify_password, create_token
from app.core.config import settings

