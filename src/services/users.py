from datetime import datetime, timezone, timedelta

import jwt
import logging
from jwt import PyJWTError
from pwdlib import PasswordHash
from asyncpg.exceptions import UniqueViolationError

from src.services.base import BaseService
from src.api.schemas.users import (
    UserCreateRequest, UserCreateSchema, UserCreateResponse
)
from src.core.config import settings
from src.exceptions.auth import InvalidTokenException
from src.exceptions.base import DataAlreadyExistsException


class PasswordService:
    password_hash = PasswordHash.recommended()

    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.password_hash.hash(password)


class TokenService:
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT.SECRET_KEY, algorithm=settings.JWT.ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, data: str):
        try:
            return jwt.decode(
                data, settings.JWT.SECRET_KEY, algorithm=settings.JWT.ALGORITHM
            )
        except PyJWTError as e:
            logging.error(e)
            raise InvalidTokenException() from e


class UserService(BaseService):
    password_service = PasswordService()
    token_service = TokenService()

    async def create_user(self, user: UserCreateRequest) -> UserCreateResponse:
        password = user.password.get_secret_value()
        validate_data = UserCreateSchema(
            email=user.email,
            hashed_password=self.password_service.get_password_hash(password)
        )
        try:
            new_user = await self.db.user.create(validate_data)
            access_token = self.token_service.create_access_token({"user_id": new_user.id})

            await self.db.commit()

        except Exception as e:
            if isinstance(getattr(e.orig, "__cause__", None), UniqueViolationError):
                raise DataAlreadyExistsException
            raise

        return UserCreateResponse(
            access_token=access_token,
            token_type="bearer",
        )
