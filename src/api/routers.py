from fastapi import APIRouter

from src.api.endpoints import users_router


main_router = APIRouter()


main_router.include_router(users_router, prefix="/auth", tags=["Auth"])
