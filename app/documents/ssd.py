from mongoengine import fields as f

from app.documents.base import BaseComponentDocument


class SsdDocument(BaseComponentDocument):
    meta = {"collection": "ssd"}

    form_factor: str = f.StringField(required=True)

    volume: int = f.IntField()
    read_speed: int = f.IntField()
    write_speed: int = f.IntField()

    controller: str = f.StringField()
    interface_m2: str = f.StringField()
    memory_type: str = f.StringField()
    nvme: bool = f.BooleanField()
    radiator: bool = f.BooleanField()
