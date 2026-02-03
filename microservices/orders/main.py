import asyncio

from microservices.orders.consumer import consumer

def main():
    #task = asyncio.to_thread(consumer.start_consuming)
    #await task
    consumer.start_consuming()

if __name__ == "__main__":
    #asyncio.run(main())
    main()


