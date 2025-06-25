from mongoengine import Document, fields as f

from app.models.cpu import CpuModel
from app.models.gpu import GpuModel
from app.models.motherboard import MotherboardModel
from app.models.psu import PsuModel
from app.models.ram import RamModel


class Build(Document):
    meta = {"db_alias": "default"}

    user_id = f.ObjectIdField(required=True)

    cpu = f.ReferenceField(CpuModel)
    ram = f.ReferenceField(RamModel)
    motherboard = f.ReferenceField(MotherboardModel)
    gpu = f.ReferenceField(GpuModel)
    psu = f.ReferenceField(PsuModel)
