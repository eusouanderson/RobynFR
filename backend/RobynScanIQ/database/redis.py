from redis import Redis
from typing import Optional

from RobynScanIQ.config.env import settings


class RedisConnection:
    def __init__(self):
        self.connection: Optional[Redis] = None

    def connect(self):
        try:
            self.connection = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                username=settings.REDIS_USERNAME or None,
                password=settings.REDIS_PASSWORD or None,
                decode_responses=settings.REDIS_DECODE_RESPONSES,
            )
            self.connection.ping()
            print(" Conectado ao Redis com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar ao Redis: {e}")
            self.connection = None

    def get_client(self) -> Optional[Redis]:
        if not self.connection:
            self.connect()
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            print("🔌 Conexão com Redis encerrada.")
