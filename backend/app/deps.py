from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.core.security import decode_token


def get_db():
    """
    Yields a database session.
    This function is a dependency that can be used by FastAPI endpoints.
    It will create a new database session if one does not already exist.
    The session will be closed when the endpoint is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_id(authorization: str = Header(default="")) -> int:
    """
    Returns the ID of the current user.

    This function takes an `Authorization` header as an argument and returns the ID of the user associated with the token.

    If the token is missing, invalid, or of an incorrect type, an HTTPException is raised with a status code of 401.

    :param authorization: The `Authorization` header containing the bearer token.
    :return: The ID of the current user.
    :raises HTTPException: If the token is missing, invalid, or of an incorrect type.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = decode_token(token)
    
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    return int(payload["sub"])
