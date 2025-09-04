from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.core.security import verify_password
from app.schemas.user_schema import (
    UserAuthSchema,
    UserOutSchema,
    UserUpdateSchema,
    UserSchema,
)
from app.repos import user_repo


class UserService:
    @staticmethod
    def create_user(user: UserAuthSchema) -> UserOutSchema:
        user = user_repo.create(user)
        return user

    @staticmethod
    async def authenticate(email: str, password: str) -> UserSchema | None:
        user = user_repo.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None

        return user

    @staticmethod
    async def get_user_by_email(email: str) -> UserSchema | None:
        user = user_repo.get_by_email(email=email)
        return user

    @staticmethod
    async def get_user_by_id(id: MongoObjectId) -> UserSchema | None:
        user = user_repo.get_by_id(id=id)
        return user

    @staticmethod
    async def update_user(id: MongoObjectId, data: UserUpdateSchema) -> UserSchema:
        user = user_repo.update(id=id, data=data)
        return user
