from fastapi import APIRouter
from app.api.api_v1.handlers.chat import chat_router
from app.api.api_v1.handlers.components import component_router
from app.api.api_v1.handlers.config import config_router
from app.api.api_v1.handlers.user import user_router
from app.api.auth.jwt import auth_router

router = APIRouter()

router.include_router(chat_router, prefix="/chat", tags=["chats"])
router.include_router(component_router, prefix="/component", tags=["components"])
router.include_router(config_router, prefix="/config", tags=["configurations"])
router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
