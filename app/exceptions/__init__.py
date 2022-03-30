from fastapi import FastAPI

from .api import APIException, on_api_exception


def register_exceptions(app: FastAPI):
    app.add_exception_handler(APIException, on_api_exception)