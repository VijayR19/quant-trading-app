from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, regex=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")


class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    Token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class PredictRequest(BaseModel):
    symbol: str
    horizon_minutes: int = 30

class PredictResponse(BaseModel):
    symbol: str
    horizon_minutes: int
    predicted_price: float
    confidence: float

