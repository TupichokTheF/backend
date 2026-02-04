import asyncio

from microservices.orders.consumer import consumer

async def main():
    task = asyncio.to_thread(consumer.start_consuming)
    await task

if __name__ == "__main__":
    asyncio.run(main())


