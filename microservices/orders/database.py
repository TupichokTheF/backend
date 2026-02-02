from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base
from microservices.orders.settings import settings

import redis

from contextlib import contextmanager

class DataBase:

    def __init__(self):
        self._engine = create_engine(str(settings.DATABASE_URL))
        self._session = sessionmaker(self._engine)

    @contextmanager
    def session(self):
        with self._session() as ses:
            yield ses

    def init_database(self):
        with self._engine.begin() as connection:
            connection.run_sync(Base.metadata.create_all)

    def dispose(self):
        self._engine.dispose()

database = DataBase()
redis = redis.Redis()

def main():
    database.init_database()

if __name__ == "__main__":
    main()
