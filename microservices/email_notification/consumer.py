import pika, json
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from microservices.email_notification.service import NotificationService

class RabbitConsumer:

    def __init__(self):
        self._notification_service = NotificationService()

    def start_consuming(self):
        self._make_connection()

    def _make_connection(self):
        with pika.BlockingConnection(pika.ConnectionParameters()) as connection:
            with connection.channel() as channel:
                self._consume_message(channel)

    def _consume_message(self, channel: BlockingChannel):
        channel.basic_consume(
            queue="notifications",
            on_message_callback=self._proces_message
        )
        channel.start_consuming()

    def _proces_message(self,
                        ch: BlockingChannel,
                        method: Basic.Deliver,
                        properties: BasicProperties,
                        body: bytes
                        ):
        data = json.loads(body)
        self._notification_service.send_email(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

consumer = RabbitConsumer()