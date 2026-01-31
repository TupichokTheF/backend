import redis, asyncio
from collections import UserDict


r = redis.Redis()


class Cart(UserDict):

    def __init__(self, user_id: int):
        super().__init__()
        self._user_id = user_id
        self._decode_data()

    def _decode_data(self):
        redis_data = r.hgetall(f"cart:{self._user_id}")
        self.data = {key.decode(): val.decode() for key, val in redis_data.items()}

    def get_data(self):
        return self.data

if __name__ == "__main__":
    cart = dict()
    cart[1] = 2
    cart[2] = 3
    keys, vals = cart.items()
    print(cart.items())