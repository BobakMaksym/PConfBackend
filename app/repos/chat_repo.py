from agents import trace
from pymongo.collection import Collection
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.core import exceptions as e
from app.core.config import settings
from app.schemas.chat_schema import ChatSchema
from app.prompt import messages


class ChatRepo:

    def __init__(self, db):
        self.col: Collection = db["chats"]

    def create(self, user_id: MongoObjectId, config_id: MongoObjectId) -> ChatSchema:
        chat = ChatSchema(
            id=config_id,
            config_id=config_id,
            user_id=user_id,
            trace_id=trace(settings.WORKFLOW_NAME).trace_id,
            messages=[{"role": "assistant", "content": messages.START_MESSAGE}],
        )
        res = self.col.insert_one(chat.model_dump(by_alias=True))
        chat.id = res.inserted_id

        return chat

    def delete(self, chat_id: MongoObjectId):
        return self.col.delete_one({"_id": chat_id})

    def get_user_chat(self, user_id: MongoObjectId) -> list[ChatSchema]:
        chats = self.col.find({"user_id": user_id}, {"messages": 0})

        return [ChatSchema(**chat) for chat in chats]

    def get_chat(self, chat_id: MongoObjectId):
        _chat = self.col.find_one({"_id": chat_id})
        chat = ChatSchema(**_chat)
        messages = []
        for msg in chat.messages:
            msg_type = msg.get("type")
            if msg_type in ("message", None):
                messages.append(msg)
        chat.messages = messages
        # chat.messages = [
        #     msg for msg in chat.messages if msg.get("type") in ("message", None)
        # ]
        return chat.model_dump(by_alias=True)

    def update_history(self, chat_id: MongoObjectId, message: str):
        """просто додати повідомлення"""

        result = self.col.find_one_and_update(
            {"_id": chat_id},
            {"$push": {"messages": message}},
        )
        if not result:
            raise e.DocumentDoesNotExist
        return result
