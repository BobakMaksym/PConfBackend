from typing_extensions import Annotated
from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from bson import ObjectId


def check_object_id(value: str) -> str:
    if not ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")
    return ObjectId(value)


ObjectIdStr = Annotated[str, AfterValidator(check_object_id)]
ObjectIdBson = Annotated[ObjectId, 1]


class Example(BaseModel):
    id: ObjectIdStr


print(Example(id="5f9b3b3b9d9f3d0001a3b3b3"))
# print(Example(id=_ObjectId()))
# print(Example(id="1"))
