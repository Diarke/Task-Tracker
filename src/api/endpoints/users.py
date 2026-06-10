from fastapi import APIRouter, status, Response

from src.api.schemas.users import (
    UserCreateRequest,
    UserCreateResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserRefreshTokenRequest,
    UserRefreshTokenResponse,
    UserDBSchema,
    UserResponseSchema,
)
from src.api.dependencies.db import DBDep
from src.services.users import UserService
from src.api.api_decorators.users import set_auth_cookies
from src.api.dependencies.users import CurrentUserDep
from src.core.config import settings


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
@set_auth_cookies
async def login(user: UserLoginRequest, db: DBDep, response: Response):
    return await UserService(db).login(user)


from fastapi import HTTPException, Cookie

@router.post(
    "/refresh/",
    status_code=status.HTTP_200_OK,
    summary="refresh token",
    response_model=UserRefreshTokenResponse
)
@set_auth_cookies
async def refresh(db: DBDep, response: Response, refresh_token: str | None = Cookie(default=None)):
    if refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
    return await UserService(db).refresh_token(refresh_token)


@router.get(
    "/me/",
    status_code=status.HTTP_200_OK,
    summary="current user",
    response_model=UserResponseSchema
)
async def get_me(current_user: CurrentUserDep):
    return current_user


@router.post("/logout")
async def logout(response: Response, current_user: CurrentUserDep):
    cookie_params = dict(
        httponly=True,
        secure=settings.COOKIE.SECURE,
        samesite=settings.COOKIE.SAMESITE,
    )
    response.delete_cookie(key="access_token", **cookie_params)
    response.delete_cookie(key="refresh_token", **cookie_params)
    return {"message": "Successfully logged out"}
