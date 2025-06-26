from mongoengine import fields as f

from app.models.base import BaseDocument


class PsuDocument(BaseDocument):
    meta = {"collection": "psu"}

    form_factor = f.StringField(required=True)
    power = f.IntField(required=True)

    mb_and_cpu_powersupply = f.StringField(required=True)

    efficiency = f.IntField()
    plus_12v = f.IntField()

    pci_e_8pin_6_2 = f.IntField()
    pci_e_16pin = f.IntField()
    pci_e_6pin = f.IntField()
    pci_e_8pin = f.IntField()

    # декор
    cable_system = f.StringField()
    certification = f.StringField()
    cooling_system = f.StringField()
    fan_bearing = f.StringField()

    # інфа
    manufacturers_warranty = f.IntField()
    dimensions = f.StringField()
