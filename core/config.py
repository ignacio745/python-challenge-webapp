from pydantic import BaseSettings
from pathlib import Path

env_path = Path(".")/".env"


class Settings(BaseSettings):
    db_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    cookie_name: str

    class Config:
        env_file = env_path

settings = Settings()