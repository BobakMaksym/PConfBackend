from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.configs.typesense_config import get_client, component_schemas
from app.db import connect_mongoengine
from app.repos.component_repo import component_repos
from app.repos.index_repo import SearchIndexRepo
from app.services.sync_index_service import SyncSearchIndex


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Mongoengine
    connect_mongoengine()

    # Typesense
    index = SyncSearchIndex(
        db_repos=component_repos,
        index_repo=SearchIndexRepo(client=get_client()),
        coll_schemas=component_schemas,
    )
    index.create_coll_all()
    index.sync_coll_all()

    yield

    index.drop_all()
