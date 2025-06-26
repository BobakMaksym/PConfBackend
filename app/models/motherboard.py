from mongoengine import fields as f

from app.models.base import BaseDocument


class MotherboardDocument(BaseDocument):
    meta = {"collection": "motherboard"}

    socket = f.StringField(required=True)
    form_factor = f.StringField(required=True)
    ram_type = f.StringField(required=True)
    ram_slots = f.IntField(required=True)
    m2_count = f.IntField()

    chipset = f.StringField(required=True)

    lighting = f.BooleanField()
    vrm_heatsink = f.BooleanField()
    wifi = f.BooleanField()
