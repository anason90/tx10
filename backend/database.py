"""Database configuration and session utilities."""
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = "sqlite:///./realestate.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, future=True
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
