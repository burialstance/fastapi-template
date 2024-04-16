from contextlib import asynccontextmanager

from fastapi import FastAPI

from src import api
from src.config import settings
from src.containers import AppContainer


@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
    container: AppContainer = getattr(app.state, 'container')
    await container.database().db().create_tables()

    if init_resources := container.init_resources():
        await init_resources

    yield

    if shutdown_resources := container.shutdown_resources():
        await shutdown_resources


def create_app(**kwargs) -> FastAPI:
    _app = FastAPI(
        debug=settings.app.debug,
        title=settings.app.title,
        description=settings.app.desc,
        version=settings.app.version,
        lifespan=fastapi_lifespan,
        **kwargs
    )
    _app.state.container = AppContainer()

    api.register(_app)
    return _app


app = create_app()
