from typing import TYPE_CHECKING
import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

if TYPE_CHECKING:
    from pymongo.typings import _Pipeline

    from change_processor import IChangeProcessor

from schemas import Change

logger = logging.getLogger(__name__)


class AsyncMongo:

    def __init__(self, connection_str: str, database: str, **kwargs):
        self._client = AsyncIOMotorClient(host=connection_str, **kwargs)
        self._database: AsyncIOMotorDatabase = self._client[database]

    @property
    def database(self) -> AsyncIOMotorDatabase:
        return self._database

    @property
    def client(self) -> AsyncIOMotorClient:
        return self._client

    async def watch_changes(self, processor: "IChangeProcessor", pipeline: "_Pipeline"):
        async with self.database.watch(
            pipeline, full_document="updateLookup"
        ) as stream:
            async for raw_change in stream:
                try:
                    change = Change(**raw_change)
                except Exception:
                    logger.exception("Failed to parse Change from raw_change; skipping")
                    continue

                await processor.process(change)
