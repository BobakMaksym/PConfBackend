from fastapi import APIRouter, Depends, status, Path
from fastapi.responses import Response
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.api.deps.user_deps import get_current_user, config_owner
from app.helpers import COLLECTIONS
from app.schemas.user_schema import User
from app.repos import chat_repo
from app.services.config_service import ConfigService
from app.schemas.pc_config_schema import PcConfigId

config_router = APIRouter()

config_service = ConfigService()


id_example = {"example": "683b7ab21fbad55848727e64"}


@config_router.post("/create", summary="Create a new PC configuration")
async def create_config(current_user: User = Depends(get_current_user)):
    # creating a configuration
    config_id = config_service.create(user_id=current_user.id)
    # creating a chat for configuration
    chat_repo.create(current_user.id, config_id)

    return PcConfigId(id=config_id).model_dump(mode="json")


@config_router.get("/get/{id}", summary="Get the current state of the PC configuration")
async def get_config(
    id: MongoObjectId = Path(..., **id_example),
    current_user: User = Depends(config_owner),
):
    config = config_service.get(id)
    return config.model_dump(mode="json", exclude_none=True)


@config_router.delete("/delete/{id}")
async def delete_config(
    id: MongoObjectId = Path(), current_user: User = Depends(config_owner)
):
    config_service.delete(id)
    chat_repo.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@config_router.post(
    "/add/{id}/{component}/{component_id}", summary="Add components to a PC build"
)
async def add_component(
    id: MongoObjectId = Path(**id_example),
    component: COLLECTIONS = Path(),
    component_id: MongoObjectId = Path(
        examples=["68266380ffe1e50a2f71147a", "68266380ffe1e50a2f711452"]
    ),
    current_user: User = Depends(config_owner),
):
    build = config_service.add_component(id, component, component_id)
    return build.model_dump(mode="json")


@config_router.delete(
    "/remove/{id}/{component}",
    summary="Remove a component from the PC configuration",
)
async def remove_component(
    id: MongoObjectId = Path(**id_example),
    component: COLLECTIONS = Path(),
    current_user: User = Depends(config_owner),
):
    config_service.remove_component(id, component)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
