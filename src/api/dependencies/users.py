from typing import Annotated

import jwt
from fastapi import Cookie, Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from src.core.config import settings
from src.api.schemas.users import UserDBSchema
from src.services.base import BaseService
from src.api.dependencies.db import DBDep
from src.exceptions.users import UserNotFoundException


class TokenData(BaseModel):
    user_id: int


class _Users(BaseService):
    async def get_by_id(self, user_id: int):
        db_user = await self.db.user.get_by_id(user_id)
        if not db_user:
            raise UserNotFoundException()
        return db_user


async def get_current_user(
    db: DBDep,
    access_token: str | None = Cookie(default=None),
) -> UserDBSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if access_token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(access_token, settings.JWT.SECRET_KEY, algorithms=[settings.JWT.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception
    user = await _Users(db).get_by_id(user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[UserDBSchema, Depends(get_current_user)]