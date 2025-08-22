from bson import ObjectId
import json

from fastapi.responses import JSONResponse
from pydantic_extra_types.mongo_object_id import MongoObjectId


def json_encoder(obj):
    """Recursively converts `ObjectId` model fields to `str`"""

    if isinstance(obj, list):
        return [json_encoder(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: json_encoder(value) for key, value in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, MongoObjectId):
        return str(obj)
    else:
        return obj


# class MongoJSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, ObjectId):
#             return str(obj)
#         # додаткові обробки інших типів (якщо треба)
#         return super().default(obj)


# class CustomJSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, ObjectId):
#             return str(obj)
#         return json.JSONEncoder.default(self, obj)
