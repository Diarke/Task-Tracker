from pydantic import BaseModel, EmailStr, SecretStr, field_validator


class CreateUser(BaseModel):
    email: EmailStr
    password: SecretStr

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: SecretStr):
        if len(v.get_secret_value().strip()) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v
