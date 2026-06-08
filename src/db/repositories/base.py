from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data):
        query = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(query)
        return self.mapper.map_to_domain_entity(result.scalars().one())
