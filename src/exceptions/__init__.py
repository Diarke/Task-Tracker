from fastapi import FastAPI

from src.exceptions.base import register_exception_handlers as register_base_handlers
from src.exceptions.auth import register_exception_handlers as register_auth_handlers
from src.exceptions.users import register_exception_handlers as register_user_handlers


def register_exception_handlers(app: FastAPI):
    register_base_handlers(app)
    register_auth_handlers(app)
    register_user_handlers(app)
