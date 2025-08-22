from fastapi import APIRouter, Depends, status, Path
from fastapi.responses import Response
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.api.deps.user_deps import get_current_user
from app.db import db
from app.helpers import COLLECTIONS
from app.documents.user_model import User
from app.repos.config_repo import ConfigRepo
from app.services.config_service import ConfigService
from app.schemas.pc_config_schema import PcConfigId

config_router = APIRouter()

config_service = ConfigService()

config_repo = ConfigRepo(db=db)


@config_router.post("/create", summary="Create a new PC build")
async def create_build(current_user: User = Depends(get_current_user)):
    build_id = config_service.create(user_id=current_user.id)
    return PcConfigId(id=build_id).model_dump(mode="json")


@config_router.get(
    "/get/{config_id}", summary="Get the current state of the PC configuration"
)
async def get_config(
    config_id: MongoObjectId = Path(..., example="683b7ab21fbad55848727e64"),
    current_user: User = Depends(get_current_user),
):
    config = config_repo.get_config(config_id)
    if config:
        if config["user_id"] == current_user.id:
            config = config_service.get(config_id)
            return config.model_dump(mode="json", exclude_none=True)
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@config_router.delete("/delete/{build_id}")
async def delete_build(
    build_id: MongoObjectId = Path(), current_user: User = Depends(get_current_user)
):
    build = config_repo.get_config(build_id)
    if build:
        if build["user_id"] == current_user.id:
            build_id = config_service.delete(build_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@config_router.post(
    "/add/{build_id}/{component}/{component_id}", summary="Add components to a PC build"
)
async def add_component(
    build_id: MongoObjectId = Path(example="683b7ab21fbad55848727e64"),
    component: COLLECTIONS = Path(),
    component_id: MongoObjectId = Path(
        examples=["68266380ffe1e50a2f71147a", "68266380ffe1e50a2f711452"]
    ),
    current_user: User = Depends(get_current_user),
):
    build = config_repo.get_config(build_id)
    if build:
        if build["user_id"] == current_user.id:
            build = config_service.add_component(build_id, component, component_id)
            return build.model_dump(mode="json")
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@config_router.delete(
    "/remove/{build_id}/{component}",
    summary="Remove a component from the PC configuration",
)
async def remove_component(
    build_id: MongoObjectId = Path(example="683b7ab21fbad55848727e64"),
    component: COLLECTIONS = Path(),
    current_user: User = Depends(get_current_user),
):
    build = config_repo.get_config(build_id)
    if build:
        if build["user_id"] == current_user.id:
            config_service.remove_component(build_id, component)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    return Response(status_code=status.HTTP_404_NOT_FOUND)
