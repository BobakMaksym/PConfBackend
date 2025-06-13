from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body, Path
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError

from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings
from app.schemas.auth_schema import TokenPayload, TokenSchema
from app.schemas.user_schema import UserOut
from app.schemas.component_schema import Build
from app.services.user_service import UserService
from app.services.config_service import BuildService
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
from app.schemas.pyobjectid import PyObjectId
from app.db import db

config_router = APIRouter()

service = BuildService(db)


@config_router.post(
    "/get/{id}",
    summary="Get the current state of the PC configuration",
)
async def get_config(
    id: PyObjectId = Path(example="683b7ab21fbad55848727e64"),
    # current_user: User = Depends(get_current_user),
) -> Build:
    configuration = service.get_configuration(id)

    return configuration.model_dump()


# @auth_router.post(
#     "/test-token", summary="Test if the access token is valid", response_model=UserOut
# )
# async def test_token(user: User = Depends(get_current_user)):
#     return user


# @auth_router.post("/refresh", summary="Refresh token", response_model=TokenSchema)
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
