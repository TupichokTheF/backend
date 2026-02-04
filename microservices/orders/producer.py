import pika, json
from pika.adapters.blocking_connection import BlockingChannel

from microservices.orders.settings import settings

class RabbitProducer:

    def produce_message(self, queue: str, message: dict):
        with pika.BlockingConnection(settings.RMQ_CONNECTION) as connection:
            with connection.channel() as channel:
                self._push_message(channel, queue, message)

    def _push_message(self, channel: BlockingChannel, queue_: str, message: dict):
        queue = channel.queue_declare(queue=queue_)
        print("message published: ", message)
        channel.basic_publish(
            exchange="",
            routing_key=queue_,
            body=json.dumps(message).encode()
        )