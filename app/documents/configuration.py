from mongoengine import Document, fields as f, NULLIFY

from app.documents.cpu import CpuDocument
from app.documents.gpu import GpuDocument
from app.documents.motherboard import MotherboardDocument
from app.documents.psu import PsuDocument
from app.documents.ram import RamDocument


class ConfigDocument(Document):
    meta = {"db_alias": "default"}

    user_id = f.ObjectIdField(required=True)

    cpu = f.ReferenceField(CpuDocument, reverse_delete_rule=NULLIFY)
    ram = f.ReferenceField(RamDocument, reverse_delete_rule=NULLIFY)
    motherboard = f.ReferenceField(MotherboardDocument, reverse_delete_rule=NULLIFY)
    gpu = f.ReferenceField(GpuDocument, reverse_delete_rule=NULLIFY)
    psu = f.ReferenceField(PsuDocument, reverse_delete_rule=NULLIFY)
