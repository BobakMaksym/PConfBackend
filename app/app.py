from contextlib import asynccontextmanager
import logging
import time

from beanie import init_beanie
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from mongoengine import connect, disconnect

from app.api.api_v1.router import router
from app.core.config import settings
from app.documents.user_model import User


logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # configure_logging(level=settings.LOG_LEVEL)

    logger.critical(f"----------- демонстрація кастомних логів -----------")

    logger.info("Starting app")

    # Ініціалізація сервісів на стартапі
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).components
    await init_beanie(database=db_client, document_models=[User])

    connect(db=settings.DATABASE, host=settings.MONGO_CONNECTION_STRING)

    yield

    disconnect()

    logger.info("Finished app")

    # Вимикання сервісів на shutdown (опційно)
    # await db_client.close()  # якщо необхідно явно закривати


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    # response.headers["X-Process-Time"] = str(process_time)

    # if logger.isEnabledFor(settings.LOG_LEVEL):

    # logger.critical("Request handling time %s", round(process_time, 4))

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_V1_STR)
