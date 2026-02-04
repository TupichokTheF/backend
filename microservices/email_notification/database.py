from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from microservices.email_notification.models import Base
from microservices.email_notification.settings import settings
from microservices.email_notification import models

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
        Base.metadata.create_all(bind=self._engine)

    def dispose(self):
        self._engine.dispose()

database = DataBase()
redis = redis.Redis()

def main():
    database.init_database()
    with database.session() as ses:
        query = select(models.User)
        res = ses.execute(query)
        print(res)

if __name__ == "__main__":
    main()
