import bson
import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status as s, Body, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
from pymongo import errors as mongo_err

from app.api.deps.user_deps import get_current_user
from app.services.chat_service import ChatService
from app.documents.user_model import User
from app.schemas.pyobjectid import PyObjectId
from app.schemas.chat_schema import ChatSchema
from app.repo import ChatRepo, BuildRepo
from app.db import db
from app.core import exceptions as e
from app.core import utils

# from app.core.config import settings
# from app.schemas.auth_schema import TokenPayload
# from pydantic import ValidationError
# from jose import jwt

config_repo = BuildRepo(db)
chat_repo = ChatRepo(db)


chat_router = APIRouter()


@chat_router.post("/new/{config_id}", status_code=s.HTTP_201_CREATED)
async def create_chat(
    config_id: PyObjectId = Path(example="683b7ab21fbad55848727e64"),
    current_user: User = Depends(get_current_user),
) -> ChatSchema:
    # перевіряю, чи існує конфігурація
    config = config_repo.get_config(config_id)
    if not config:
        raise e.ConfigDoesNotExistException

    # створюю чат, якщо його ще не існує
    try:
        chat: ChatSchema = chat_repo.create(current_user.id, config_id)
    except mongo_err.DuplicateKeyError:
        return Response("A chat with this id already exists", s.HTTP_409_CONFLICT)
    return chat


@chat_router.get("/my/")
async def my_chats(current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    chats = chat_repo.get_user_chat(user_id)

    return utils.json_encoder(chats)


@chat_router.delete("/delete/{chat_id}")
async def delete_chat(
    chat_id: PyObjectId = Path(example="683b7ab21fbad55848727e64"),
    current_user: User = Depends(get_current_user),
):
    chat = chat_repo.get_chat(chat_id)
    if chat:
        # перевірка, чи це чат користувача
        if chat["user_id"] == current_user.id:
            chat_repo.delete(chat_id)
            return Response(status_code=s.HTTP_204_NO_CONTENT)
        return Response(
            "You do not have permission to access this resource",
            s.HTTP_403_FORBIDDEN,
        )
    return Response("There is no such chat", s.HTTP_404_NOT_FOUND)


@chat_router.post("/send/{chat_id}")
async def send_message(
    chat_id: PyObjectId = Path(example="683b7ab21fbad55848727e64"),
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
    chat_id: PyObjectId = Path(example="683b7ab21fbad55848727e64"),
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
