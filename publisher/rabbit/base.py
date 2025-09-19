import logging

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel

from rabbit.exceptions import RabbitException


logger = logging.getLogger(__name__)


class RabbitContext:
    def __init__(self, connection_params: ConnectionParameters):
        self.connection_params = connection_params
        self._connection: BlockingConnection | None = None
        self._channel: BlockingChannel | None = None

    @property
    def channel(self) -> "BlockingChannel":
        if self._channel is None:
            raise RabbitException("Please use context manager for Rabbit helper.")
        return self._channel

    def __enter__(self):
        self._connection = BlockingConnection(parameters=self.connection_params)
        self._channel = self._connection.channel()

        return self

    def __exit__(self, exc_type, value, traceback):
        if not self._channel:
            return

        if self._channel.is_open:
            self._channel.close()

        if not self._connection:
            return

        if self._connection.is_open:
            self._connection.close()
