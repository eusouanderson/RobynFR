from typing import Any

from redis import Redis

from RobynScanIQ.config.env import settings


class RedisConnection:
    DEFAULT_TTL = 3600

    def __init__(self):
        self.connection: Redis | None = None

    def connect(self) -> Redis:
        """Conecta ao Redis se ainda não conectado e retorna a instância."""
        if self.connection is None:
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
                print('✅ Conectado ao Redis com sucesso!')
            except Exception as e:
                raise ConnectionError(f'Erro ao conectar ao Redis: {e}')
        return self.connection

    def set(self, key: str, value: Any, ttl: int | None = None):
        """Define uma chave com TTL padrão se não for informado."""
        redis_client = self.connect()
        ttl_to_use = ttl if ttl is not None else self.DEFAULT_TTL
        redis_client.set(name=key, value=value, ex=ttl_to_use)

    def get(self, key: str) -> str | None:
        """Recupera o valor de uma chave."""
        redis_client = self.connect()
        return redis_client.get(key)

    def delete(self, key: str):
        """Deleta uma chave do Redis."""
        redis_client = self.connect()
        redis_client.delete(key)

    def close(self):
        """Fecha a conexão com o Redis."""
        if self.connection:
            self.connection.close()
            self.connection = None
            print('🔌 Conexão com Redis encerrada.')
