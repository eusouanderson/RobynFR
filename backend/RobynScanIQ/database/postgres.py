from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from RobynScanIQ.config.env import settings

engine = create_engine(settings.db_url, echo=settings.DEBUG, future=True)
SessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, class_=Session
)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Função que retorna uma sessão do SQLAlchemy como generator."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
