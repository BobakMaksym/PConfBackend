import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

from config import config as conf
from rabbit.base import RabbitContext


logger = logging.getLogger(__name__)


class ComponentUpdateMixin:
    channel: "BlockingChannel"

    def create_queue(self, queue_name: str = conf.RABBIT_ROUTING_KEY):
        self.channel.queue_declare(queue=queue_name)

    def publish_message(self, message: str):

        self.channel.basic_publish(
            exchange="",  # conf.RABBIT_EXCHANGE,
            routing_key=conf.RABBIT_ROUTING_KEY,
            body=message,  # type: ignore
        )

        logger.info("%s", message)


class ComponentUpdateRabbit(ComponentUpdateMixin, RabbitContext):
    pass
