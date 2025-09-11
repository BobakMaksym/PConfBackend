from app.documents.configuration import ConfigDocument
from app.documents.cpu import CpuDocument
from app.documents.gpu import GpuDocument
from app.documents.motherboard import MotherboardDocument
from app.documents.psu import PsuDocument
from app.documents.ram import RamDocument
from app.documents.user import UserDocument


component_docs = {
    "cpu": CpuDocument,
    "gpu": GpuDocument,
    "motherboard": MotherboardDocument,
    "psu": PsuDocument,
    "ram": RamDocument,
}

__all__ = (
    component_docs,
    ConfigDocument,
    CpuDocument,
    GpuDocument,
    MotherboardDocument,
    PsuDocument,
    RamDocument,
    UserDocument,
)
