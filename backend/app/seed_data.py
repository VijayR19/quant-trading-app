"""

Seed initial data for local development and testing.

"""
from sqlalchemy.orm import Session, session
from app.db import Base, engine, SessionLocal
from app.models import User
from app.core.security import hash_password

def seed_initial_users(session: Session) -> None:
    """
    Seed initial users into the database.

    :param session: The database session.
    """
    Base.metadata.create_all(bind=engine)
    session.query(User).delete()  # Clear existing data

    initial_users_data = [

        {"email": "test@tradingapp.com", "password": "Test@1234"},
        {"email": "admin@tradingapp.com", "password": "Admin@1234"},
    ]

    for initial_user_data in initial_users_data:
        existing_user = session.query(User).filter_by(email=initial_user_data["email"]).first()
        if not existing_user:
            user = User(
                email=initial_user_data["email"],
                hashed_password=hash_password(initial_user_data["password"])
            )
            session.add(user)
    session.commit()


if __name__ == "__main__":
  seed_initial_users()