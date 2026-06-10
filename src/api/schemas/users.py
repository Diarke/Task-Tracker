from datetime import datetime

from typing import Annotated
from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    field_validator,
    Field,
)


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str


class UserCreateRequest(BaseModel):
    email: Annotated[EmailStr, Field(description="User email address")]
    password: Annotated[SecretStr, Field(description="User password")]

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: SecretStr):
        if len(v.get_secret_value().strip()) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserCreateSchema(BaseModel):
    email: EmailStr
    hashed_password: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr


class UserLoginResponse(TokenPairSchema):
    ...


class UserDBSchema(BaseModel):
    id: Annotated[int, Field(description="Unique user identifier")]
    email: Annotated[EmailStr, Field(description="User email address")]
    hashed_password: Annotated[str, Field(description="Hashed user password")]
    is_admin: Annotated[bool, Field()]
    is_active: Annotated[bool, Field()]
    created_at: Annotated[datetime, Field(description="Timestamp when the user was created")]
    updated_at: Annotated[datetime, Field(description="Timestamp when the user was last updated")]


class UserResponseSchema(BaseModel):
    id: Annotated[int, Field(description="Unique user identifier")]
    email: Annotated[EmailStr, Field(description="User email address")]
    is_active: Annotated[bool, Field()]
    created_at: Annotated[datetime, Field(description="Timestamp when the user was created")]
    updated_at: Annotated[datetime, Field(description="Timestamp when the user was last updated")]


class UserCreateResponse(TokenPairSchema):
    ...


class UserRefreshTokenRequest(BaseModel):
    refresh_token: str


class UserRefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
