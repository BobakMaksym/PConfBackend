from fastapi import APIRouter, Depends, status, Path
from fastapi.responses import Response

from app.api.deps.user_deps import get_current_user
from app.core import utils
from app.db import db
from app.helpers import COLLECTIONS
from app.models.user_model import User
from app.repo import BuildRepo
from app.services.component_service import ConfigService
from app.schemas.component_schema import Build
from app.schemas.user_schema import UserOut
from app.services.config_service import BuildService
from app.services.user_service import UserService
from app.schemas.pyobjectid import PyObjectId

config_router = APIRouter()

service = BuildService(db)
config_service = ConfigService()


@config_router.post("/create", summary="Create a new PC build")
async def create_build(current_user: User = Depends(get_current_user)):
    build_id = ConfigService().create_build(user_id=current_user.id)
    return {"_id": str(build_id)}


@config_router.get(
    "/get/{config_id}",
    summary="Get the current state of the PC configuration",
)
async def get_config(
    config_id: PyObjectId = Path(..., example="683b7ab21fbad55848727e64"),
    current_user: User = Depends(get_current_user),
):
    config = BuildRepo(db).get_config(config_id)
    if config:
        if config["user_id"] == current_user.id:
            config = service.get_configuration(config_id)
    return utils.json_encoder(config.model_dump(by_alias=True, exclude_none=True))


@config_router.delete("/delete/{build_id}")
async def delete_build(
    build_id: PyObjectId = Path(), current_user: User = Depends(get_current_user)
):
    build = BuildRepo(db).get_config(build_id)
    if build:
        if build["user_id"] == current_user.id:
            build_id = ConfigService().delete_build(build_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@config_router.post(
    "/add/{build_id}/{component}/{component_id}", summary="Add components to a PC build"
)
async def add_component(
    build_id: PyObjectId = Path(example="683b7ab21fbad55848727e64"),
    component: COLLECTIONS = Path(),
    component_id: PyObjectId = Path(
        examples=["68266380ffe1e50a2f71147a", "68266380ffe1e50a2f711452"]
    ),
    current_user: User = Depends(get_current_user),
):
    build = BuildRepo(db).get_config(build_id)
    if build:
        if build["user_id"] == current_user.id:
            build = config_service.add_component(build_id, component, component_id)
            return utils.json_encoder(build.model_dump(by_alias=True))
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@config_router.delete(
    "/remove/{build_id}/{component}",
    summary="Remove a component from the PC configuration",
)
async def remove_component(
    build_id: PyObjectId = Path(example="683b7ab21fbad55848727e64"),
    component: COLLECTIONS = Path(),
    current_user: User = Depends(get_current_user),
):
    build = BuildRepo(db).get_config(build_id)
    if build:
        if build["user_id"] == current_user.id:
            ConfigService().remove_component(build_id, component)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    return Response(status_code=status.HTTP_404_NOT_FOUND)
