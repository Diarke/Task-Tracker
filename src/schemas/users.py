from datetime import datetime

from typing import Annotated
from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    field_validator,
    Field,
)


class CreateUser(BaseModel):
    email: Annotated[EmailStr, Field(description="User email address")]
    password: Annotated[SecretStr, Field(description="User password")]

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: SecretStr):
        if len(v.get_secret_value().strip()) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class User(BaseModel):
    id: Annotated[int, Field(description="Unique user identifier")]
    email: Annotated[EmailStr, Field(description="User email address")]
    hashed_password: Annotated[str, Field(description="Hashed user password")]
    created_at: Annotated[datetime, Field(description="Timestamp when the user was created")]
    updated_at: Annotated[datetime, Field(description="Timestamp when the user was last updated")]
