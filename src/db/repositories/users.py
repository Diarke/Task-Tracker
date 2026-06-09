from sqlalchemy import select

from src.db.repositories.base import BaseRepository
from src.db.models.users import UsersORM
from src.db.repositories.mappers.users import UserDataMapper


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_by_email(self, email: str) -> UsersORM | None:
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        return self.mapper.map_to_domain_entity(result.scalars().one_or_none())
