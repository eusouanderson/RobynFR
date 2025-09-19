from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from RobynScanIQ.config.env import settings

engine = create_engine(settings.DB_URL, echo=settings.DEBUG, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=Session)
Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
