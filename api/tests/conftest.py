"""Shared test fixtures.

Strategy: tests run against a real Postgres database named ``booking_test`` on
the same server as the development database. Once per test run the schema is
dropped and rebuilt from the Alembic migrations, so tests always exercise the
same DDL as production. Between tests every table is truncated. Truncation
rather than transaction rollback is deliberate: the double-booking tests open
several connections at once, which a single rolled-back transaction cannot model.
"""

from collections.abc import Iterator

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

import app.models  # noqa: F401  (registers every table on Base.metadata for truncation)
from app.config import settings
from app.db import Base, get_db
from app.main import create_app

TEST_DATABASE_NAME = "booking_test"


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """Ensure the test database exists and return its URL."""
    url = make_url(settings.database_url)
    admin_url = url.set(database="postgres").render_as_string(hide_password=False)
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": TEST_DATABASE_NAME},
        ).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{TEST_DATABASE_NAME}"'))
    admin_engine.dispose()
    return url.set(database=TEST_DATABASE_NAME).render_as_string(hide_password=False)


@pytest.fixture(scope="session")
def engine(test_database_url: str) -> Iterator[Engine]:
    """Rebuild the test schema from migrations once per run."""
    engine = create_engine(test_database_url)
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_database_url)
    command.upgrade(alembic_cfg, "head")

    yield engine
    engine.dispose()


@pytest.fixture
def db(engine: Engine) -> Iterator[sessionmaker[Session]]:
    """A session factory bound to the test database. Tables are truncated after each test."""
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    yield factory

    tables = [table.name for table in reversed(Base.metadata.sorted_tables)]
    if tables:
        quoted = ", ".join(f'"{name}"' for name in tables)
        with engine.begin() as conn:
            conn.execute(text(f"TRUNCATE {quoted} RESTART IDENTITY CASCADE"))


@pytest.fixture
def client(db: sessionmaker[Session]) -> TestClient:
    """An HTTP client for the app, wired to the test database."""
    app = create_app()

    def override_get_db() -> Iterator[Session]:
        with db() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
