from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

import pika

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        extra="ignore",
    )
    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=self.POSTGRES_DB
        )

    RMQ_HOST: str = ""
    RMQ_PORT: int = 5672
    @property
    def RMQ_CONNECTION(self):
        return pika.ConnectionParameters(host=self.RMQ_HOST, port=self.RMQ_PORT)

settings = Settings()