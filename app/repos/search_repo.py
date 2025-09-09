from typesense.client import Client

from logging import getLogger

from app.core.configs.typesense_config import ComponentCollections, schemas, config_dict


logger = getLogger("app")


client = Client(config_dict=config_dict)


def init_collections_in_typesense():
    """initialize collections in typesense if they do not exist"""
    for collection in ComponentCollections:
        try:
            client.collections[collection].retrieve()
            logger.info("%s collection already created in typesense", collection)
        except Exception:
            client.collections.create(schemas[collection])
            logger.info("%s collection was created in typesense", collection)
