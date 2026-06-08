from fastapi import APIRouter, status

from src.api.schemas.users import UserCreateRequest
from src.api.dependencies.db import DBDep
from src.services.users import UserService


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="create user",
)
async def register(user: UserCreateRequest, db: DBDep):
    return await UserService(db).create_user(user)

