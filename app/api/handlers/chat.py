from typing import Annotated

from fastapi import APIRouter, Depends, status, Body, Path
from fastapi.responses import Response, JSONResponse
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.api.deps.user_deps import get_current_user, get_chat_if_owner, ChatWithOwner
from app.services.chat_service import ChatService
from app.schemas.chat_schema import ChatSchema
from app.schemas.user_schema import User
from app.repos import chat_repo


chat_router = APIRouter()

ChatIfOwnerDeps = Annotated[ChatWithOwner, Depends(get_chat_if_owner)]


@chat_router.get("/my/")
async def my_chats(current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    chats = chat_repo.get_user_chat(user_id)

    return [chat.model_dump(mode="json") for chat in chats]


@chat_router.delete("/clear/{id}")
async def clear_chat(
    deps: ChatIfOwnerDeps,
    id: MongoObjectId = Path(example="683b7ab21fbad55848727e64"),
):
    chat_repo.clear(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@chat_router.post("/send/{id}")
async def send_message(
    deps: ChatIfOwnerDeps,
    id: MongoObjectId = Path(example="683b7ab21fbad55848727e64"),
    message: str = Body(),
):
    response = await ChatService().send_message(id, message)
    return JSONResponse(response, status.HTTP_201_CREATED)


@chat_router.get("/get/{id}", response_model=ChatSchema)
async def get_chat(
    deps: ChatIfOwnerDeps,
    id: MongoObjectId = Path(example="683b7ab21fbad55848727e64"),
):
    return deps.chat
