from mongoengine import Document, fields as f, NULLIFY

from app.documents.cpu import CpuModel
from app.documents.gpu import GpuModel
from app.documents.motherboard import MotherboardModel
from app.documents.psu import PsuModel
from app.documents.ram import RamModel


class ConfigDocument(Document):
    meta = {"db_alias": "default"}

    user_id = f.ObjectIdField(required=True)

    cpu = f.ReferenceField(CpuModel, reverse_delete_rule=NULLIFY)
    ram = f.ReferenceField(RamModel, reverse_delete_rule=NULLIFY)
    motherboard = f.ReferenceField(MotherboardModel, reverse_delete_rule=NULLIFY)
    gpu = f.ReferenceField(GpuModel, reverse_delete_rule=NULLIFY)
    psu = f.ReferenceField(PsuModel, reverse_delete_rule=NULLIFY)
