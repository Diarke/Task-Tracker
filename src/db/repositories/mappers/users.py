from src.db.repositories.mappers.base import DataMapper
from src.db.models.users import UsersORM
from src.schemas.users import User


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User
