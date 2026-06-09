from fastapi import APIRouter, status

from src.api.schemas.users import (
    UserCreateRequest,
    UserCreateResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserRefreshTokenRequest,
    UserRefreshTokenResponse,
)
from src.api.dependencies.db import DBDep
from src.services.users import UserService


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="create user",
    response_model=UserCreateResponse
)
async def register(user: UserCreateRequest, db: DBDep):
    return await UserService(db).create_user(user)


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    summary="login",
    response_model=UserLoginResponse
)
async def login(user: UserLoginRequest, db: DBDep):
    return await UserService(db).login(user)


@router.post(
    "/refresh/",
    status_code=status.HTTP_200_OK,
    summary="get refresh token",
    response_model=UserRefreshTokenResponse
)
async def refresh(token: UserRefreshTokenRequest, db: DBDep):
    return await UserService(db).refresh_token(token)
