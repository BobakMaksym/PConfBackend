from mongoengine import fields as f

from app.documents.base import BaseDocument


class GpuDocument(BaseDocument):
    meta = {"collection": "gpu"}

    model_gpu = f.StringField(required=True)
    memory_size = f.IntField(required=True)
    memory_type = f.StringField(required=True)
    monitors = f.IntField()
    power_consumption = f.IntField(required=True)
    additional_power = f.StringField()
    fans = f.IntField()
    lighting = f.BooleanField()
