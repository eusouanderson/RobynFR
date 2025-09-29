# pylint: skip-file
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

from RobynScanIQ.config.env import settings
from RobynScanIQ.database.postgres import Base


from RobynScanIQ.models.document_model import Document

# Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# metadata para autogenerate
target_metadata = Base.metadata
print("METADATA tables:", target_metadata.tables.keys())


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=settings.db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(settings.db_url, poolclass=pool.NullPool, future=True)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
