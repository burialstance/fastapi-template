from functools import lru_cache
from pathlib import Path

import tzlocal
from pydantic import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    APP_TITLE: str = 'appTitle'
    APP_DESC: str = 'asicBrute'
    APP_VERSION: str = '0.1'

    DEBUG: bool = True
    BASE_DIR: Path = BASE_DIR
    LOG_PATH: Path = BASE_DIR.parent.joinpath('logs/logs.log')
    APPLICATIONS_DIR: Path = BASE_DIR.joinpath('applications')

    TIMEZONE = tzlocal.get_localzone_name()
    DATABASE_URI = 'sqlite://database.sqlite'

    API_ROUTE_PREFIX = '/api'
    SECRET_KEY = 'qweasdqweasd'  # openssl rand -hex 32
    CRYPT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

    CORS_ORIGINS = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:5000",
        "http://localhost:3000",
    ]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]

    class Config:
        env_prefix = ''
        env_file = BASE_DIR.parent.joinpath('.env')


@lru_cache
def _build_settings():
    return Settings()


settings = _build_settings()
