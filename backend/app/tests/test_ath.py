import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models import User
from app.schemas import UserCreate
from app.core.security import hash_password
from app.routers.auth import register

def test_register_existing_email(db: Session):
    # Arrange
    user = User(email="test@example.com", hashed_password="hashed_password")
    db.add(user)
    db.commit()

    payload = UserCreate(email="test@example.com", password="password")

    # Act
    with pytest.raises(HTTPException) as exc_info:
        register(payload, db)

    # Assert
    assert exc_info.value.detail == "Email already registered"

def test_register_new_user(db: Session):
    # Arrange
    payload = UserCreate(email="newuser@example.com", password="password")

    # Act
    result = register(payload, db)

    # Assert
    assert result.email == "newuser@example.com"
    assert result.hashed_password is not None

def test_register_with_db_error(db: Session):
    # Arrange
    original_add = db.add

    def raise_db_error_side_effect(*args, **kwargs):
        raise Exception("Database error")

    db.add = raise_db_error_side_effect

    payload = UserCreate(email="newuser@example.com", password="password")

    # Act
    with pytest.raises(Exception) as exc_info:
        register(payload, db)

    # Assert
    assert str(exc_info.value) == "Database error"

    # Clean up
    db.add = original_add
