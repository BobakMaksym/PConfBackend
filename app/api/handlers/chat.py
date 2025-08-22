from fastapi import APIRouter, Depends, status as s, Body, Path
from fastapi.responses import Response, JSONResponse
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.api.deps.user_deps import get_current_user
from app.services.chat_service import ChatService
from app.documents.user_model import User
from app.schemas.chat_schema import ChatSchema
from app.repos.chat_repo import ChatRepo
from app.repos.config_repo import ConfigRepo
from app.db import db

# from app.core.config import settings
# from app.schemas.auth_schema import TokenPayload
# from pydantic import ValidationError
# from jose import jwt

config_repo = ConfigRepo(db=db)
chat_repo = ChatRepo(db=db)


chat_router = APIRouter()


@chat_router.get("/my/")
async def my_chats(current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    chats = chat_repo.get_user_chat(user_id)

    return [chat.model_dump(mode="json") for chat in chats]


@chat_router.delete("/clear/{id}")
async def clear_chat(
    id: MongoObjectId = Path(example="683b7ab21fbad55848727e64"),
    current_user: User = Depends(get_current_user),
):
    chat = chat_repo.get_chat(id)
    if chat:
        # перевірка, чи це чат користувача
        if chat["user_id"] == current_user.id:
            chat_repo.clear(id)
            return Response(status_code=s.HTTP_204_NO_CONTENT)
        return Response(
            "You do not have permission to access this resource",
            s.HTTP_403_FORBIDDEN,
        )
    return Response("There is no such chat", s.HTTP_404_NOT_FOUND)


@chat_router.post("/send/{chat_id}")
async def send_message(
    chat_id: MongoObjectId = Path(example="683b7ab21fbad55848727e64"),
    message: str = Body(),
    current_user: User = Depends(get_current_user),
):
    chat = chat_repo.get_chat(chat_id)
    if chat:
        # перевірка, чи це чат користувача
        if chat["user_id"] == current_user.id:

            response = await ChatService().send_message(chat_id, message)

            return JSONResponse(response, s.HTTP_201_CREATED)
        return Response(
            "You do not have permission to access this resource",
            s.HTTP_403_FORBIDDEN,
        )
    return Response("There is no such chat", s.HTTP_404_NOT_FOUND)


@chat_router.get("/get/{chat_id}")
async def get_chat(
    chat_id: MongoObjectId = Path(example="683b7ab21fbad55848727e64"),
    current_user: User = Depends(get_current_user),
):
    chat = chat_repo.get_chat(chat_id)
    if chat:
        # перевірка, чи це чат користувача
        if chat["user_id"] == current_user.id:
            return ChatSchema(**chat)

        return Response(
            "You do not have permission to access this resource",
            s.HTTP_403_FORBIDDEN,
        )
    return Response("There is no such chat", s.HTTP_404_NOT_FOUND)
