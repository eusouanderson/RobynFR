import os

from dotenv import load_dotenv

load_dotenv()


class SettingsEnv:
    """Classe para carregar e armazenar variáveis de ambiente."""

    # PostgreSQL
    DB_USER: str = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'password')
    DB_NAME: str = os.getenv('DB_NAME', 'postgresDB')
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '5432'))

    # Application
    APP_HOST: str = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT: int = int(os.getenv('APP_PORT', '8080'))
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() in {'true', '1', 'yes'}

    # Redis
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_USERNAME: str = os.getenv('REDIS_USERNAME', '')
    REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD', '')
    REDIS_DB: int = int(os.getenv('REDIS_DB', '0'))
    REDIS_DECODE_RESPONSES: bool = os.getenv(
        'REDIS_DECODE_RESPONSES', 'True'
    ).lower() in {'true', '1', 'yes'}

    # IA / Gemini
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')

    @property
    def db_url(self) -> str:
        """Retorna a URL completa de conexão com PostgreSQL."""
        return (
            f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@'
            f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )


settings = SettingsEnv()
