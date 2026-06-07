from functools import cached_property, lru_cache

from typing import Annotated, Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


class AppSettings(ModelConfig):
    DEBUG: Annotated[bool, Field()]
    TITLE: Annotated[str, Field()]
    SUMMARY: Annotated[str, Field()]
    DESCRIPTION: Annotated[str, Field()]
    VERSION: Annotated[str, Field()]
    DOCS_URL: Annotated[str, Field()]
    REDOC_URL: Annotated[str, Field()]


class PostgresSettings(ModelConfig):
    DB_HOST: Annotated[str, Field()]
    DB_PORT: Annotated[int, Field()]
    DB_NAME: Annotated[str, Field()]
    DB_USER: Annotated[str, Field()]
    DB_PASS: Annotated[str, Field()]

    @cached_property
    def DSN(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class JWTSettings(ModelConfig):
    SECRET_KEY: Annotated[str, Field()]
    ALGORITHM: Annotated[str, Field]
    ACCESS_TOKEN_EXPIRE_MINUTES: Annotated[int, Field()]


class Settings(ModelConfig):
    MODE: Literal["local", "dev", "prod", "test"] = "local"

    APP: AppSettings = AppSettings()
    POSTGRES: PostgresSettings = PostgresSettings()
    JWT: JWTSettings = JWTSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
