from bson import ObjectId
from pydantic import BaseModel

from app.schemas.pyobjectid import PyObjectId


class MyModel(BaseModel):
    a: PyObjectId
    b: list[PyObjectId]
    c: str

    class Config:
        json_encoders = {
            PyObjectId: lambda v: str(v),
        }


mm = MyModel(a=PyObjectId(), b=[PyObjectId(), PyObjectId()], c="qwerty")


print(mm.model_dump_json())
