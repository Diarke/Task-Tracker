from pwdlib import PasswordHash

from src.services.base import BaseService
from src.api.schemas.users import UserCreateRequest, UserCreateSchema


class PasswordService:
    password_hash = PasswordHash.recommended()

    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.password_hash.hash(password)


class UserService(BaseService):
    password_service = PasswordService()

    async def create_user(self, user: UserCreateRequest):
        password = user.password.get_secret_value()
        validate_data = UserCreateSchema(
            email=user.email,
            hashed_password=self.password_service.get_password_hash(password)
        )
        new_user = await self.db.user.create(validate_data)

        await self.db.commit()
