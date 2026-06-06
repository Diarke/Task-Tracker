from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session: AsyncSession):
        self.session = session
