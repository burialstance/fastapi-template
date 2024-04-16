import logging
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.DEBUG)

SRC_DIR = Path(__file__).parent.parent
ENV_FILE = SRC_DIR.parent.joinpath('.env')


class BaseEnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding='utf-8',
        extra='ignore'
    )


class AppSettings(BaseEnvSettings):
    debug: bool = True
    title: str = 'app_title'
    desc: str = 'app_desc'
    version: str = '0.0.1'


class DatabaseSettings(BaseEnvSettings):
    url: str = f'sqlite+aiosqlite:///{SRC_DIR.parent}/db.sqlite'
    echo: bool = True


app = AppSettings(_env_prefix='APP_')
db = DatabaseSettings(_env_prefix='DB_')
