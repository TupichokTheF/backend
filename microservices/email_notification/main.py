import asyncio

from microservices.email_notification.service import NotificationService
from microservices.email_notification.consumer import consumer

def main():
    #task = asyncio.to_thread(consumer.start_consuming, "notifications")
    #await task
    consumer.start_consuming()


if __name__ == "__main__":
    #asyncio.run(main())
    main()


