from src.db.repositories.mappers.base import DataMapper
from src.db.models.users import UsersORM
from src.api.schemas.users import UserDBSchema


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = UserDBSchema
