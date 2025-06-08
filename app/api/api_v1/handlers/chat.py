import bson
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Body

# from fastapi.security import OAuth2PasswordRequestForm

# from app.services.user_service import UserService
# from app.core.security import create_access_token, create_refresh_token
# from app.schemas.auth_schema import TokenSchema
# from app.schemas.user_schema import UserOut
from app.api.deps.user_deps import get_current_user
from app.models.user_model import User
from app.service_ai import create_chat, delete_chat

# from app.core.config import settings
# from app.schemas.auth_schema import TokenPayload
# from pydantic import ValidationError
# from jose import jwt


chat_router = APIRouter()


@chat_router.post("/new")
async def new_chat(current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    _id = create_chat(current_user.id)
    return {
        "status": status.HTTP_201_CREATED,
        "msg": f'chat created ObjectId("{_id}")',
    }


@chat_router.post("/delete")
async def new_chat(_id: str, current_user: User = Depends(get_current_user)):
    delete_chat(bson.ObjectId(_id))
    return {
        "status": status.HTTP_204_NO_CONTENT,
        "msg": f'chat ObjectId("{_id}") deleted',
    }


# @chat_router.post(
#     "/test-token", summary="Test if the access token is valid", response_model=UserOut
# )
# async def test_token(user: User = Depends(get_current_user)):
#     return user


# @chat_router.post("/refresh", summary="Refresh token", response_model=TokenSchema)
# async def refresh_token(refresh_token: str = Body(...)):
#     try:
#         payload = jwt.decode(
#             refresh_token,
#             settings.JWT_REFRESH_SECRET_KEY,
#             algorithms=[settings.ALGORITHM],
#         )
#         token_data = TokenPayload(**payload)
#     except (jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Invalid token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     user = await UserService.get_user_by_id(token_data.sub)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid token for user",
#         )
#     return {
#         "access_token": create_access_token(user.user_id),
#         "refresh_token": create_refresh_token(user.user_id),
#     }
