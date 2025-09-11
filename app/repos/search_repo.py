from logging import getLogger

from typesense.client import Client
from typesense import exceptions as e

from app.core.configs.typesense_config import ComponentCollections, schemas, config_dict
from app.schemas.base import BaseDbSchema
from app.repos.component_repo import repos, IComponentRepo


logger = getLogger("app")


client = Client(config_dict=config_dict)


class SearchSchema(BaseDbSchema):
    model: str


def drop_collection(collection: ComponentCollections):
    try:
        client.collections[collection].delete()
        logger.info("delete %s collection", collection)
    except e.ObjectNotFound:
        logger.error(
            "try to delete %s collection, but collection doesn't exist", collection
        )


def drop_all_collections():
    for collection in ComponentCollections:
        drop_collection(collection)


def init_collection(collection: ComponentCollections):
    try:
        client.collections.create(schemas[collection])
        logger.info("%s collection was created in typesense", collection)
    except e.ObjectAlreadyExists:
        logger.info("%s collection already created in typesense", collection)


def init_all_collections():
    """initialize collections in typesense if they do not exist"""
    for collection in ComponentCollections:
        init_collection(collection)


def upload_data_to_collection(
    collection: ComponentCollections,
    documents: list[SearchSchema] | None = None,
):
    repo: IComponentRepo = repos[collection]

    documents = repo.collection._get_collection().find({})

    doc_inserted_count = 0
    for doc in documents:

        doc = SearchSchema.model_validate(doc).model_dump(mode="json")
        client.collections[collection].documents.upsert(doc)
        doc_inserted_count += 1

    return {"inserted": doc_inserted_count}


def list_document_in_collection(collection: ComponentCollections):
    docs = client.collections[collection].documents.documents
    return docs


def list_collections():
    collection_info = client.collections.retrieve()
    collection_names = [coll["name"] for coll in collection_info]
    return collection_names
