from dataclasses import dataclass

from pydantic import BaseModel

from app.schemas.pyobjectid import PyObjectId


@dataclass
class BuildContext:
    _id: PyObjectId


class Components(BaseModel):
    cpu: PyObjectId | None = None
    gpu: PyObjectId | None = None
    ram: PyObjectId | None = None
    psu: PyObjectId | None = None
    motherboard: PyObjectId | None = None
