from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    app_name: str = "Trading App (TEST)"

    database_url: str = "postgresql+psycopg2://localhost/trading_app_test?sslmode=prefer"

    jwt_secret: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    jwt_algorithm: str = "HS256"

    access_token_minutes: int = 60  # longer for tests
    refresh_token_days: int = 1

    testing: bool = True


test_settings = TestSettings()
