from contextlib import asynccontextmanager
from mongoengine import connect

from fastapi import FastAPI

from app.core.config import settings
from repos.search_repo import init_collections_in_typesense


@asynccontextmanager
async def lifespan(app: FastAPI):

    # mongoengine
    connect(db=settings.DATABASE, host=settings.MONGO_CONNECTION_STRING)

    # typesense
    init_collections_in_typesense()

    yield
