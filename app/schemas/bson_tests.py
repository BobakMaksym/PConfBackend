# from bson import ObjectId

# from pydantic import BaseModel, Field


# class Schema(BaseModel):
#     id: ObjectId = Field(alias="_id")
#     user_id: ObjectId

#     class Config:
#         json_encoders = {
#             ObjectId: lambda v: str(v),
#         }


# # schema = Schema(id=ObjectId(), user_id=ObjectId())
# # print(schema)

# print(str(ObjectId()))
