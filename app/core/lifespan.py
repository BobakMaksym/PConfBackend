from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings as conf
from app.core.configs.typesense_config import get_client
from app.db import connect_mongoengine
from app.repos.component_repo import CpuRepo, GpuRepo, MbRepo, PsuRepo, RamRepo, SsdRepo
from app.repos.index_repo import (
    CpuIndexRepo,
    GpuIndexRepo,
    RamIndexRepo,
    PsuIndexRepo,
    MotherboardIndexRepo,
    SsdIndexRepo,
)
from app.use_case.sync_search_index_case import SyncSearchIndexUseCase


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Mongoengine
    connect_mongoengine()

    # Typesense
    client = get_client()

    sync_search_index_use_case = SyncSearchIndexUseCase(
        repos=[
            (CpuRepo(), CpuIndexRepo(client=client)),
            (GpuRepo(), GpuIndexRepo(client=client)),
            (RamRepo(), RamIndexRepo(client=client)),
            (PsuRepo(), PsuIndexRepo(client=client)),
            (MbRepo(), MotherboardIndexRepo(client=client)),
            (SsdRepo(), SsdIndexRepo(client=client)),
        ]
    )

    if conf.CREATE_NEW_SEARCH_INDEX_WHEN_RESTART:
        sync_search_index_use_case.create_collections()
        sync_search_index_use_case.sync_data()

    yield

    if conf.DROP_SEARCH_INDEX_WHEN_RESTART:
        sync_search_index_use_case.drop_collections()
