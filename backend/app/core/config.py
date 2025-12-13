from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Trading App"
    jwt_secret: str = "CHANGE_ME_SUPER_SECRET"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 15
    refresh_token_days: int = 14
    database_url: str = "postgresql+psycopg2://localhost/trading_app?sslmode=prefer"

settings = Settings()