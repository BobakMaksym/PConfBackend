from mongoengine import fields as f

from app.documents.base import BaseComponentDocument


class GpuDocument(BaseComponentDocument):
    meta = {"collection": "gpu"}

    model_gpu: str = f.StringField(required=True)
    memory_size: int = f.IntField(required=True)
    memory_type: str = f.StringField(required=True)
    monitors: int = f.IntField()
    power_consumption: int = f.IntField(required=True)
    additional_power: str = f.StringField()
    fans: int = f.IntField()
    lighting: bool = f.BooleanField()
