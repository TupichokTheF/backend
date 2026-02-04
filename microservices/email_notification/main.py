import asyncio

from microservices.email_notification.consumer import consumer

async def main():
    order_notifications = asyncio.to_thread(consumer.start_consuming, "notifications")
    two_factor_auth = asyncio.to_thread(consumer.start_consuming, "two_factor_auth")
    await asyncio.gather(*[asyncio.create_task(x) for x in [order_notifications, two_factor_auth]])

if __name__ == "__main__":
    asyncio.run(main())


