import pika, json
from pika.adapters.blocking_connection import BlockingChannel

from typing import Annotated

from fastapi import Depends

from app.core.settings import settings

class RabbitService:

    def produce_message(self, queue: str, message: dict):
        with pika.BlockingConnection(settings.RMQ_CONNECTION) as connection:
            with connection.channel() as channel:
                self._push_message(channel, queue, message)

    def _push_message(self, channel: BlockingChannel, queue: str, message: dict):
        queue = channel.queue_declare(queue=queue)
        channel.basic_publish(
            exchange="",
            routing_key="orders",
            body=json.dumps(message).encode()
        )

async def get_rabbit():
    return RabbitService()

RabbitDep = Annotated[RabbitService, Depends(get_rabbit)]