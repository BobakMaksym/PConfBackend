from datetime import datetime
from dataclasses import dataclass

from jose import jwt
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.core.config import settings
from app.schemas.auth_schema import TokenPayloadSchema
from app.schemas.chat_schema import ChatSchema
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema
from app.repos import config_repo, chat_repo


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login", scheme_name="JWT"
)


@dataclass
class ChatWithOwner:
    user: UserSchema
    chat: ChatSchema


async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserSchema:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayloadSchema(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserService.get_user_by_id(token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user


async def config_owner(
    id: MongoObjectId = Path(...), current_user: UserSchema = Depends(get_current_user)
):
    config = config_repo.get_config(id)

    if not config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if not config.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return current_user


async def get_chat_if_owner(
    id: MongoObjectId = Path(...), current_user: UserSchema = Depends(get_current_user)
):
    chat = chat_repo.get_chat(id)

    if not chat:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "There is no such chat")

    # перевірка, чи це чат користувача
    if not chat.user_id == current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "You do not have permission to access this resource",
        )

    return ChatWithOwner(current_user, chat)
