from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint, Numeric
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (UniqueConstraint('email', name='uq_user_email'),)
    

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    symbol = Column(String, nullable=False, index=True)
    side = Column(String, nullable=False)  # BUY or SELL
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(12, 4), nullable=False)
    status = Column(String, nullable=False, default="FILLED")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)