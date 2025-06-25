from mongoengine import fields as f

from app.models.base import BaseDocument


class GpuModel(BaseDocument):
    model_gpu = f.StringField(required=True)
    memory_size = f.IntField(required=True)
    memory_type = f.StringField(required=True)
    monitors = f.IntField()
    power_consumption = f.IntField(required=True)
    additional_power = f.StringField()
    fans = f.IntField()
    lighting = f.BooleanField()
