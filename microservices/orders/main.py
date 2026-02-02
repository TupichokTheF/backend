import asyncio

from microservices.orders.consumer import consumer
from microservices.orders.service import OrderService

def main():
    #task = asyncio.to_thread(consumer.start_consuming)
    #await task
    test = OrderService()
    test.make_order({"user_id": 1})

if __name__ == "__main__":
    main()


