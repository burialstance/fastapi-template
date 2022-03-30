from fastapi import FastAPI


from starlette.middleware.cors import CORSMiddleware

from app.applications import register_api_routes
from app.conf.logs import configure_log
from app.conf.settings import settings
from app.database import register_database
from app.exceptions import register_exceptions

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESC,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


@app.on_event('startup')
async def on_startup():
    configure_log(write=False)
    register_database(app)
    register_exceptions(app)
    register_api_routes(app)


