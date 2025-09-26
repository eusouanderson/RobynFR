from typing import Optional, Union

import redis
from redis.cluster import RedisCluster


class RedisConnection:
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 6379,
        **kwargs,
    ):
        """
        Classe para gerenciar conexões avançadas com Redis.

        Args:
            host (str): Endereço do servidor Redis.
            port (int): Porta do Redis.
            kwargs: Outros parâmetros opcionais:
                - db (int)
                - password (str)
                - url (str)
                - use_pool (bool)
                - cluster_nodes (list[dict])
        """
        self.host = host
        self.port = port
        self.db: int = kwargs.get('db', 0)
        self.password: Optional[str] = kwargs.get('password')
        self.url: Optional[str] = kwargs.get('url')
        self.use_pool: bool = kwargs.get('use_pool', False)
        self.cluster_nodes: Optional[list[dict]] = kwargs.get('cluster_nodes')
        self.connection: Optional[Union[redis.Redis, RedisCluster]] = None

    def connect(self):
        """Inicializa a conexão de acordo com a configuração"""
        try:
            if self.cluster_nodes:
                # Conexão com Redis Cluster
                self.connection = RedisCluster(
                    startup_nodes=self.cluster_nodes,
                    password=self.password,
                    decode_responses=True,
                )
            elif self.url:
                # Conexão via URL
                self.connection = redis.from_url(
                    self.url,
                    decode_responses=True,
                )
            elif self.use_pool:
                # Conexão com ConnectionPool
                pool = redis.ConnectionPool(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    password=self.password,
                    decode_responses=True,
                )
                self.connection = redis.Redis(connection_pool=pool)
            else:
                # Conexão simples
                self.connection = redis.Redis(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    password=self.password,
                    decode_responses=True,
                )

            # Teste rápido da conexão
            self.connection.ping()
            print('✅ Conectado ao Redis com sucesso!')
        except Exception as e:
            print(f'❌ Erro ao conectar ao Redis: {e}')
            self.connection = None

    def get_client(self) -> Optional[Union[redis.Redis, RedisCluster]]:
        """Retorna a instância de conexão ativa"""
        if not self.connection:
            self.connect()
        return self.connection

    def close(self):
        """Fecha a conexão com Redis"""
        if self.connection:
            self.connection.close()
            print('🔌 Conexão com Redis encerrada.')
