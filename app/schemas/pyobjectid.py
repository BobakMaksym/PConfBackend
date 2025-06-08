from typing import Any
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, info) -> ObjectId:
        # info можна ігнорувати, якщо не потрібен
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            try:
                return ObjectId(v)
            except Exception as e:
                raise ValueError(f"Invalid ObjectId: {v}") from e
        raise TypeError("ObjectId or 24-hex string expected")

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"title": "ObjectId", "type": "string", "pattern": "^[0-9a-fA-F]{24}$"}
