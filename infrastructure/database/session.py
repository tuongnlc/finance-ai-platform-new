from __future__ import annotations

import os
import time
from typing import AsyncIterator

from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()

# --- Connection config (fill these in .env) ---
ENDPOINT = os.getenv("LAKE_FLOW_ENDPOINT")  # Lakebase compute endpoint
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")  # Databricks workspace host (used by the SDK)
USERNAME = os.getenv("PGUSER")  # Postgres DB identity
DATABASE = "databricks_postgres"
PORT = 5432

_workspace = WorkspaceClient()

# --- OAuth token management ---
_token: str | None = None
_token_expiry: float = 0.0  # Unix timestamp when the current token expires


def _refresh_token() -> None:
    global _token, _token_expiry
    credential = _workspace.postgres.generate_database_credential(endpoint=ENDPOINT)
    _token = credential.token
    _token_expiry = credential.expire_time.seconds


def _provide_token(dialect, conn_rec, cargs, cparams) -> None:
    # Refresh token if None or expiring within 2 minutes
    if _token is None or time.time() >= _token_expiry - 120:
        _refresh_token()
    cparams["password"] = _token


def _resolve_host() -> str:
    """The Postgres host comes from the Lakebase compute endpoint, not the workspace host."""
    endpoint_info = _workspace.postgres.get_endpoint(name=ENDPOINT)
    return endpoint_info.status.hosts.host


# --- Async engine & session factory ---
engine = create_async_engine(
    f"postgresql+psycopg://{USERNAME}:@{_resolve_host()}:{PORT}/{DATABASE}?sslmode=require"
)
event.listens_for(engine.sync_engine, "do_connect")(_provide_token)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Async session dependency: `async for session in get_session()` or FastAPI `Depends`."""
    async with AsyncSessionLocal() as session:
        yield session


async def dispose_engine() -> None:
    """Close all pooled connections. Call on application shutdown."""
    await engine.dispose()
