from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    """Declarative base shared by every model.

    Alembic reads ``Base.metadata`` to autogenerate migrations, and the test
    suite reads it to know which tables to truncate between tests.
    """


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    """FastAPI dependency: one database session per request, closed afterwards.

    Tests override this dependency so requests hit the test database instead.
    """
    with SessionLocal() as session:
        yield session
