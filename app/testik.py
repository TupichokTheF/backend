import redis

r = redis.Redis()


if __name__ == "__main__":
    r.hset("cart:user1", mapping={
        "product1": 2,
        "product2": 1,
    })
    print(r.hgetall("cart:user1"))