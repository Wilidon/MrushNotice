from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    token: str

    db_host: str
    db_username: str
    db_password: str
    db_name: str

    name: str
    password: str

    admins = [list]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()