from src.db.repositories.base import BaseRepository
from src.db.models.users import UsersORM
from src.db.repositories.mappers.users import UserDataMapper


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper
