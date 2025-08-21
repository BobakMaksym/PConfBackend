from uuid import UUID

from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.core.security import verify_password

from app.documents.user_model import User
from app.schemas.user_schema import UserAuth, UserOut, UserUpdate

from app.repos.user_repo import UserRepo
from app.db import db


user_repo = UserRepo(db=db)


class UserService:
    @staticmethod
    def create_user(user: UserAuth) -> UserOut:
        user = user_repo.create(user)
        return user

    @staticmethod
    async def authenticate(email: str, password: str) -> User | None:
        user = user_repo.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None

        return user

    @staticmethod
    async def get_user_by_email(email: str) -> User | None:
        user = user_repo.get_by_email(email=email)
        return user

    @staticmethod
    async def get_user_by_id(id: MongoObjectId) -> User | None:
        user = user_repo.get_by_id(id=id)
        return user

    @staticmethod
    async def update_user(id: MongoObjectId, data: UserUpdate) -> User:
        user = user_repo.update(id=id, data=data)
        return user
