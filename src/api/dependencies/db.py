from typing import Annotated

from fastapi import Depends

from src.db.session import async_sessionlocal
from src.db.repositories import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.user = UsersRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()


async def get_db():
    async with DBManager(async_sessionlocal) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
