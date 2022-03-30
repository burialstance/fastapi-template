from fastapi import FastAPI

from .routes import router as root_router

from app.conf.settings import settings


def register_api_routes(app: FastAPI):
    app.include_router(root_router, prefix=settings.API_ROUTE_PREFIX)
