import asyncio
import json
import logging
from typing import AsyncContextManager

import aio_pika
from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractChannel,
    AbstractQueue,
    AbstractIncomingMessage,
)

from pydantic import ValidationError

from config import config as conf
from schemas.change import Change
from rabbit.exceptions import RabbitException


logger = logging.getLogger(__name__)


class AsyncioRabbit(AsyncContextManager):
    def __init__(self, connection_params, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.is_running = True

        self.connection_params = connection_params
        self.queue_name = conf.RABBIT_ROUTING_KEY

        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None
        self._queue: AbstractQueue | None = None

    @property
    def channel(self) -> AbstractChannel:
        if self._channel is None:
            raise RabbitException("Please use context manager for Rabbit helper.")
        return self._channel

    @property
    def connection(self) -> AbstractRobustConnection:
        if self._connection is None:
            raise RabbitException("Please use context manager for Rabbit helper.")
        return self._connection

    @property
    def queue(self) -> AbstractQueue:
        if self._queue is None:
            raise RabbitException("Please use context manager for Rabbit helper.")
        return self._queue

    async def __aenter__(self):
        await self.run()
        return self

    async def __aexit__(self, exc_type, value, traceback):
        await self.stop()

    async def run(self):
        self._connection = await aio_pika.connect_robust(self.connection_params)
        self._channel = await self._connection.channel()

        EXCHANGE_NAME = "mongo_changes"
        QUEUE_NAME = "mongo_change_queue"

        self.exchange = await self.channel.declare_exchange(
            EXCHANGE_NAME, aio_pika.ExchangeType.DIRECT, durable=True
        )
        self._queue = await self.channel.declare_queue(QUEUE_NAME, durable=True)

        await self.channel.set_qos(prefetch_count=1)

        await self.queue.bind(exchange=self.exchange, routing_key="mongo.change")

    async def stop(self):
        logger.info("Stopping publisher...")

        if not self.channel.is_closed:
            await self.channel.close()
        if not self.connection.is_closed:
            await self.connection.close()

        logger.info("Publisher stopped")

    async def publish_message(self, message):
        message_body = json.dumps(message, default=str)
        message = aio_pika.Message(body=message_body.encode())
        routing_key = "mongo.change"

        await self.exchange.publish(message, routing_key=routing_key)

    def set_message_processor(self, processor):
        self.__msg_processor = processor

    async def __on_message_callback(self, message: AbstractIncomingMessage):

        try:
            decoded_body = message.body.decode()
            body = json.loads(json.loads(decoded_body))
            change = Change(**body)
            op_type, coll, id = (
                change.operation_type.value,
                change.ns.coll,
                str(change.id),
            )
            log = "Start consuming new message from Q: operation=%r, coll=%r, id=%r; msg: %s"
            logger.info(log, op_type, coll, id, decoded_body)

            self.__msg_processor.process(change=change)
            log = "Message processing completed: operation=%r, coll=%r, id=%r"
            logger.info(log, op_type, coll, id)

            await message.ack()

        except TypeError:
            logger.error("Unable to serialize the message: %s", decoded_body)
            await message.nack(requeue=False)

        except Exception as e:
            await message.nack(requeue=True)
            logger.error(type(e))

    async def consume_messages(self):
        async with self.queue.iterator() as queue_iterator:
            async for message in queue_iterator:
                await self.__on_message_callback(message)
