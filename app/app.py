from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from mongoengine import connect, disconnect

from app.api.api_v1.router import router
from app.core.config import settings
from app.models.user_model import User


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Ініціалізація сервісів на стартапі
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).components
    await init_beanie(database=db_client, document_models=[User])

    connect(db=settings.DATABASE, host=settings.MONGO_CONNECTION_STRING)
    yield
    disconnect()
    # Вимикання сервісів на shutdown (опційно)
    # await db_client.close()  # якщо необхідно явно закривати


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_V1_STR)
