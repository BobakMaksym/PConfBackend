from datetime import datetime

from jose import jwt
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.core.config import settings
from app.schemas.auth_schema import TokenPayload
from app.services.user_service import UserService
from app.schemas.user_schema import User
from app.repos import config_repo


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login", scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

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
    id: MongoObjectId = Path(...), current_user: User = Depends(get_current_user)
):
    config = config_repo.get_config(id)

    if not config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if not config.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return current_user
