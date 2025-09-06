from mongoengine import fields as f

from app.documents.base import BaseComponentDocument


class MotherboardDocument(BaseComponentDocument):
    meta = {"collection": "motherboard"}

    socket: str = f.StringField(required=True)
    form_factor: str = f.StringField(required=True)
    ram_type: str = f.StringField(required=True)
    ram_slots: int = f.IntField(required=True)
    m2_count: int = f.IntField()

    chipset: str = f.StringField(required=True)

    lighting: bool = f.BooleanField()
    vrm_heatsink: bool = f.BooleanField()
    wifi: bool = f.BooleanField()
