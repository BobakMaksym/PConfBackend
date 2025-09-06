from mongoengine import fields as f

from app.documents.base import BaseComponentDocument


class RamDocument(BaseComponentDocument):
    meta = {"collection": "ram"}

    type: str = f.StringField(required=True)
    modules: int = f.IntField(required=True)
    capacity: int = f.IntField(required=True)
    speed: int = f.IntField(required=True)

    cooling: bool = f.BooleanField()
    colour: str = f.StringField()
    lighting: bool = f.BooleanField()
