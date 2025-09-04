from fastapi import APIRouter, Depends

from app.api.deps.user_deps import get_current_user
from app.core import db_exceptions as db_exc
from app.core import exceptions as api_exc
from app.schemas.user_schema import (
    UserAuthSchema,
    UserOutSchema,
    UserUpdateSchema,
    UserSchema,
)
from app.services.user_service import UserService


user_router = APIRouter()


@user_router.post("/create", summary="Create new user", response_model=UserOutSchema)
def create_user(data: UserAuthSchema):
    try:
        return UserService.create_user(data)
    except db_exc.EmailDuplicateError:
        raise api_exc.EmailIsAlreadyInUseException
    except db_exc.UsernameDuplicateError:
        raise api_exc.UsernameIsAlreadyInUseException


@user_router.get(
    "/me",
    summary="Get details of currently logged in user",
    response_model=UserOutSchema,
)
async def get_me(user: UserSchema = Depends(get_current_user)):
    return user


@user_router.post("/update", summary="Update User", response_model=UserOutSchema)
async def update_user(
    data: UserUpdateSchema, user: UserSchema = Depends(get_current_user)
):
    try:
        return await UserService.update_user(user.id, data)
    except db_exc.NotFoundError:
        raise api_exc.UserDoesNotExistException
    except db_exc.EmailDuplicateError:
        raise api_exc.EmailIsAlreadyInUseException
    except db_exc.UsernameDuplicateError:
        raise api_exc.UsernameIsAlreadyInUseException
