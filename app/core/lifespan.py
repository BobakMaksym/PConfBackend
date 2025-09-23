from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings as conf
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

    search_index = SearchIndexRepo(client=get_client())
    sync_search_index = SyncSearchIndex(
        db_repos=component_repos,
        index_repo=search_index,
        coll_schemas=component_schemas,
    )

    app.state.search_index = search_index
    app.state.sync_search_index = sync_search_index

    if conf.CREATE_NEW_SEARCH_INDEX_WHEN_RESTART:
        sync_search_index.create_coll_all()
        sync_search_index.sync_coll_all()

    yield

    if conf.CREATE_NEW_SEARCH_INDEX_WHEN_RESTART:
        sync_search_index.drop_all()
