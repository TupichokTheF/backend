import redis

r = redis.Redis()


if __name__ == "__main__":
    res = r.zrange(name="score", start=0, end=-1)
    print(res)