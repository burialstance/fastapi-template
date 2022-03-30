from fastapi import FastAPI
from tortoise import Tortoise
from loguru import logger
from tortoise.contrib.fastapi import register_tortoise

from .config import TORTOISE_CONFIG


async def database_init():
    await Tortoise.init(TORTOISE_CONFIG)
    await Tortoise.generate_schemas()
    logger.info("Tortoise inited!")


async def database_close():
    await Tortoise.close_connections()
    logger.info("Tortoise closed!")


def register_database(app: FastAPI):
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        generate_schemas=True,
        add_exception_handlers=True,
    )
