from mongoengine import fields as f

from app.documents.base import BaseComponentDocument


class PsuDocument(BaseComponentDocument):
    meta = {
        "collection": "psu",
        "strict": False,
    }

    form_factor: str = f.StringField(required=True)
    power: int = f.IntField(required=True)

    mb_and_cpu_powersupply: str = f.StringField(required=True)

    efficiency: int = f.IntField()
    plus_12v: int = f.IntField()

    pci_e_8pin_6_2: int = f.IntField()
    pci_e_16pin: int = f.IntField()
    pci_e_6pin: int = f.IntField()
    pci_e_8pin: int = f.IntField()

    # декор
    cable_system: str = f.StringField()
    certification: str = f.StringField()
    cooling_system: str = f.StringField()
    fan_bearing: str = f.StringField()

    # інфа
    manufacturers_warranty: int = f.IntField()
    dimensions: str = f.StringField()
