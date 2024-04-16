from fastapi import APIRouter, FastAPI

from . import v1

root_router = APIRouter()
root_router.include_router(v1.router, prefix='/v1')


def register(app: FastAPI):
    app.include_router(root_router, prefix='/api')
