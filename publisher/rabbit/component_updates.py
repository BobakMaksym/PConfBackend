import logging
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties

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

    def consume_messages(
        self,
        on_message_callback: Callable[
            [
                "BlockingChannel",
                "Basic.Deliver",
                "BasicProperties",
                bytes,
            ],
            None,
        ],
    ):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.queue_declare(conf.RABBIT_ROUTING_KEY)
        self.channel.basic_consume(
            queue=conf.RABBIT_ROUTING_KEY,
            on_message_callback=on_message_callback,
        )
        self.channel.start_consuming()


class ComponentUpdateRabbit(ComponentUpdateMixin, RabbitContext):
    pass
