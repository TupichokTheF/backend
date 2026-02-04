import pika, json
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from microservices.orders.service import OrderService
from microservices.orders.producer import RabbitProducer

class RabbitConsumer:

    def __init__(self):
        self._order_service = OrderService()
        self._message_producer = RabbitProducer()

    def start_consuming(self):
        self._make_connection()

    def _make_connection(self):
        with pika.BlockingConnection(pika.ConnectionParameters()) as connection:
            with connection.channel() as channel:
                self._consume_message(channel)

    def _consume_message(self, channel: BlockingChannel):
        channel.basic_consume(
            queue="orders",
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
        message = {
            "receiver": "maks.belopolov@mail.ru",
            "title": "OZON market",
            "type": "notification",
            "message": "Ваш заказ в пути!"
        }
        try:
            self._order_service.make_order(data)
        except Exception as e:
            message["message"] = "Ваш заказ отменен."
        self._message_producer.produce_message("notifications", message)
        ch.basic_ack(delivery_tag=method.delivery_tag)

consumer = RabbitConsumer()