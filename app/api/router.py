from fastapi import APIRouter

from app.api.handlers.chat import chat_router
from app.api.handlers.components import component_router
from app.api.handlers.config import config_router
from app.api.handlers.jwt import auth_router
from app.api.handlers.user import user_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(chat_router, prefix="/chat", tags=["chats"])
router.include_router(config_router, prefix="/config", tags=["configurations"])
router.include_router(component_router, prefix="/component", tags=["components"])
