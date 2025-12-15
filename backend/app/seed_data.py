"""

Seed initial data for local development and testing.

"""
from sqlalchemy.orm import Session
from app.db import Base, engine, SessionLocal
from app.models import User
from app.core.security import hash_password

def seed_initial_users(db: Session) -> None:
    """
    Seed initial users into the database.

    :param db: The database session.
    """
    Base.metadata.create_all(bind=engine)
    db.query(User).delete()  # Clear existing data

    initial_users_data = [

        User(email="test@tradingapp.com",  hashed_password="Test@1234"),
        User(email="admin@tradingapp.com",  hashed_password="Admin@1234"),
    ]

    for initial_user_data in initial_users_data:
        existing_user = db.query(User).filter_by(email=initial_user_data.email).first()
        if not existing_user:
            user = User(
                email=initial_user_data.email,
                hashed_password=hash_password(initial_user_data.hashed_password),
            )
            db.add(user)
    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_initial_users(db)
    finally:
        db.close()