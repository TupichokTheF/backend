import redis, asyncio

r = redis.Redis()

async def main():
    r.zadd(name="score", mapping={f"product:{3}": 1})

if __name__ == "__main__":
    asyncio.run(main())
    #print(res)