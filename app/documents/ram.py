from mongoengine import fields as f

from app.documents.base import BaseDocument


class RamDocument(BaseDocument):
    meta = {"collection": "ram"}

    type = f.StringField(required=True)
    modules = f.IntField(required=True)
    capacity = f.IntField(required=True)
    speed = f.IntField(required=True)

    cooling = f.BooleanField()
    colour = f.StringField()
    lighting = f.BooleanField()
