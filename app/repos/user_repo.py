import logging

import pymongo
from pymongo.collection import Collection
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.core import exceptions as e
from app.core.security import get_password
from app.schemas.user_schema import UserAuth, UserOut, UserUpdate, User
from app.core import db_exceptions as db_err


logger = logging.getLogger("app")


class UserRepo:
    def __init__(self, db):
        self.col: Collection = db["users"]

    def create(self, user: UserAuth) -> User:
        db_users = self.col.find(
            {"$or": [{"username": user.username}, {"email": user.email}]}
        )
        for db_user in db_users:
            if db_user["email"] == user.email:
                raise db_err.EmailDuplicateError
            elif db_user["username"] == user.username:
                raise db_err.UsernameDuplicateError

        hashed_password = get_password(user.password)
        user_doc = user.model_dump(exclude_none=True, exclude={"password"})
        user_doc["hashed_password"] = hashed_password

        self.col.insert_one(user_doc)

        return User(**user_doc)

    def get_by_email(self, email: str) -> User | None:
        user = self.col.find_one({"email": email})
        return User(**user) if user else None

    def get_by_id(self, id: MongoObjectId) -> User | None:
        user = self.col.find_one({"_id": id})
        return User(**user) if user else None

    def update(self, id: MongoObjectId, data: UserUpdate) -> User:
        user = self.col.find_one_and_update(
            {"_id": id},
            {"$set": data.model_dump(exclude_unset=True)},
            return_document=True,
        )
        if not user:
            raise db_err.NotFoundError

        return User(**user)
