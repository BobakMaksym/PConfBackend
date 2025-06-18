# from bson import ObjectId
# from pydantic import BaseModel

# from app.schemas.pyobjectid import PyObjectId


# class MyModel(BaseModel):
#     a: PyObjectId
#     b: list[PyObjectId]
#     c: str

#     class Config:
#         json_encoders = {
#             PyObjectId: lambda v: str(v),
#         }


# mm = MyModel(a=PyObjectId(), b=[PyObjectId(), PyObjectId()], c="qwerty")


# print(mm.model_dump_json())


import abc
from bson import ObjectId

from pydantic import BaseModel, Field

from app.core.utils import json_encoder
from app.rules_engine.manager import rule_manager
from app.schemas.pyobjectid import PyObjectId


class BaseComponentModel(abc.ABC, BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)

    # @property
    # def _id(self):
    #     return PyObjectId(self.id)

    class Config:
        json_encoders = {
            PyObjectId: lambda v: str(v),
        }


class Cpu(BaseComponentModel):
    manufacturer: str | None = Field(default=None)


class Ram(BaseComponentModel):
    manufacturer: str


class Build(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)

    cpu: Cpu | None = None
    ram: Ram | None = None

    class Config:
        json_encoders = {
            PyObjectId: lambda v: str(v),
        }


if __name__ == "__main__":

    cpu = Cpu(_id=PyObjectId(), manufacturer="AMD")
    ram = Ram(_id=PyObjectId(), manufacturer="Corsair")

    build = Build(_id=PyObjectId(), cpu=cpu, ram=ram)

    print(build)
    print(build.model_dump_json(by_alias=True))
    # print(type(build.model_dump_json()))

    print(json_encoder(build.model_dump()))
