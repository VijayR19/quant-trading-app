from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


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


from pydantic import BaseModel, Field

class TradeCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=16)
    side: str = Field(pattern="^(BUY|SELL)$")
    quantity: int = Field(gt=0)

class TradeRead(BaseModel):
    id: int
    symbol: str
    side: str
    quantity: int
    price: float
    status: str

    class Config:
        from_attributes = True

class PositionRead(BaseModel):
    symbol: str
    quantity: int

class PnLRead(BaseModel):
    symbol: str
    quantity: int
    avg_entry: float
    last_price: float
    unrealized_pnl: float
