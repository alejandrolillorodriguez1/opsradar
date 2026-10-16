from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: SecretStr
    db_name: str


@lru_cache
def get_settings() -> Settings:
    return Settings()