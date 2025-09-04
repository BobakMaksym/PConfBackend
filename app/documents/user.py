from datetime import datetime
from typing import Self

from mongoengine import Document, fields as f


class UserDocument(Document):
    meta = {"collection": "users"}

    username = f.StringField(unique=True, required=True)
    email = f.EmailField(unique=True, required=True)
    hashed_password = f.StringField(required=True)
    first_name = f.StringField()
    last_name = f.StringField()
    disabled = f.BooleanField()
    created_at = f.DateTimeField(required=True, default=datetime.now)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.email})"

    def __str__(self) -> str:
        return self.email

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Self):
            return self.email == other.email
        return False
