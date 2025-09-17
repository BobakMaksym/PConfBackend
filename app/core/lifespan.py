from contextlib import asynccontextmanager
from mongoengine import connect

from fastapi import FastAPI

from app.core.config import settings
from app.repos.search_repo import (
    CpuIndexRepo,
    GpuIndexRepo,
    RamIndexRepo,
    PsuIndexRepo,
    MotherboardIndexRepo,
    client,
)
from app.services.sync_index_service import TsCollectionInitializer


@asynccontextmanager
async def lifespan(app: FastAPI):

    # mongoengine
    connect(db=settings.DATABASE, host=settings.MONGO_CONNECTION_STRING)

    # typesense
    ts_coll_init_service = TsCollectionInitializer(
        CpuIndexRepo(client=client),
        GpuIndexRepo(client=client),
        RamIndexRepo(client=client),
        PsuIndexRepo(client=client),
        MotherboardIndexRepo(client=client),
    )
    ts_coll_init_service.init_all()

    yield

    ts_coll_init_service.drop_all()
