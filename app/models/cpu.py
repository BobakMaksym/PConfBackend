from mongoengine import fields as f

from app.models.base import BaseDocument


class CpuDocument(BaseDocument):
    meta = {"collection": "cpu"}

    socket: str = f.StringField(required=True)
    ram_types: str = f.StringField(required=True)
    igp: bool = f.BooleanField(required=True)
    tdp: int = f.IntField(required=True)
    tdp_max: int = f.IntField()
    cores: int = f.IntField(required=True)
    threads: int = f.IntField(required=True)
