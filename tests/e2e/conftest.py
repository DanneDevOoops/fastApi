import pytest
import pytest_asyncio
from httpx2 import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

from src.db.config.base import Base  # ← real Base with models registered on it
from src.db.connectors.postgres_db import get_pg_db
from src.db.models.v1_models.applications_model_v1 import (  # noqa: F401 — registers table
    Application,
)
from src.db.models.v1_models.users_model_v1 import User  # noqa: F401 — registers table
from src.main import app


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16.9-alpine") as pg:
        yield pg


@pytest_asyncio.fixture(scope="function")  # ← function scope avoids event loop mismatch
async def db_engine(postgres_container):
    sync_url = postgres_container.get_connection_url()
    async_url = sync_url.replace("psycopg2", "asyncpg")

    engine = create_async_engine(async_url, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # now actually creates tables

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    session_factory = async_sessionmaker(db_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def e2e_client(db_session):
    async def override_get_db():
        yield db_session

    _original = app.dependency_overrides.get(get_pg_db)
    app.dependency_overrides[get_pg_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
    # Restore whatever was there before (e.g. SQLite override from root conftest)
    if _original is not None:
        app.dependency_overrides[get_pg_db] = _original
    else:
        app.dependency_overrides.pop(get_pg_db, None)
