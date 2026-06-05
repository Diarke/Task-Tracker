from typing import Any, AsyncGenerator

import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import settings


logger = logging.getLogger(__name__)

engine = create_async_engine(settings.POSTGRES.DSN, echo=False)

async_sessionlocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_sessionlocal() as session:
        yield session


async def check_db_connection():
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT version()"))
        logger.info("Версия базы данных: %s", res.fetchone())
