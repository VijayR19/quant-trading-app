from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Trading App"

    jwt_secret: str = "CHANGE_ME_SUPER_SECRET"
    jwt_algorithm: str = "HS256"

    access_token_minutes: int = 15
    refresh_token_days: int = 14

    db_user: str
    db_password: str
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:"
            f"{self.db_password}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
