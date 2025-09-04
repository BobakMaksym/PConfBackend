import logging

from pydantic_extra_types.mongo_object_id import MongoObjectId
from mongoengine.queryset.visitor import Q

from app.core import exceptions as e
from app.core import db_exceptions as db_err
from app.core.security import get_password
from app.documents import UserDocument
from app.schemas.user_schema import UserAuthSchema, UserUpdateSchema, UserSchema


logger = logging.getLogger("app")


class UserRepo:
    def __init__(self, db=None):
        """the method is no longer needed, it remains only to preserve the interface"""
        pass

    def create(self, user: UserAuthSchema) -> UserSchema:
        # Verification of username and email uniqueness
        existing = UserDocument.objects(
            Q(email=user.email) | Q(username=user.username)
        ).first()
        if existing:
            if existing.email == user.email:
                raise db_err.EmailDuplicateError
            elif existing.username == user.username:
                raise db_err.UsernameDuplicateError

        user_doc = UserDocument(
            **user.model_dump(exclude_none=True, exclude=["password"]),
            hashed_password=get_password(user.password),
        )
        user_doc.save()

        return UserSchema.model_validate(user_doc)

    def get_by_email(self, email: str) -> UserSchema | None:
        user = UserDocument.objects.get(email=email)
        return UserSchema.model_validate(user) if user else None

    def get_by_id(self, id: MongoObjectId) -> UserSchema | None:
        user = UserDocument.objects.get(id=id)
        return UserSchema.model_validate(user) if user else None

    def update(self, id: MongoObjectId, data: UserUpdateSchema) -> UserSchema:
        update_data = data.model_dump(exclude_none=True)

        user = UserDocument.objects(id=id).modify(
            new=True,
            **{f"set__{k}": v for k, v in update_data.items()},
        )
        if not user:
            raise db_err.NotFoundError

        return UserSchema.model_validate(user)
