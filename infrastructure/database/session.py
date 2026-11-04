from __future__ import annotations

import os
import time
from typing import AsyncIterator

from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

load_dotenv()

# --- Connection config (fill these in .env) ---
ENDPOINT = os.getenv("LAKE_FLOW_ENDPOINT")  # Lakebase compute endpoint
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")  # Databricks workspace host (used by the SDK)
# Local: lấy PGUSER từ .env (email của bạn)
# Trên app: PGUSER không set -> dùng DATABRICKS_CLIENT_ID do runtime inject
USERNAME = os.getenv("PGUSER") or os.getenv("DATABRICKS_CLIENT_ID")
DATABASE = "databricks_postgres"
PORT = 5432

_workspace: WorkspaceClient | None = None


def _get_workspace() -> WorkspaceClient:
    """Create the Databricks client on first use instead of at import time."""
    global _workspace
    if _workspace is None:
        _workspace = WorkspaceClient()
    return _workspace

# --- OAuth token management ---
_token: str | None = None
_token_expiry: float = 0.0  # Unix timestamp when the current token expires


def _refresh_token() -> None:
    global _token, _token_expiry
    credential = _get_workspace().postgres.generate_database_credential(endpoint=ENDPOINT)
    _token = credential.token
    _token_expiry = credential.expire_time.seconds


def _provide_token(dialect, conn_rec, cargs, cparams) -> None:
    # Refresh token only when missing or expiring within 2 minutes.
    # This listener is fully synchronous, so it runs atomically w.r.t. the event loop:
    # concurrent connections reuse the same cached token instead of each fetching one.
    if _token is None or time.time() >= _token_expiry - 120:
        _refresh_token()
    cparams["password"] = _token


def _resolve_host() -> str:
    """The Postgres host comes from the Lakebase compute endpoint, not the workspace host."""
    endpoint_info = _get_workspace().postgres.get_endpoint(name=ENDPOINT)
    return endpoint_info.status.hosts.host


# --- Async engine & session factory (lazy singletons) ---
_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def _get_engine() -> AsyncEngine:
    """Build the engine once, on first use (no network calls at import time).

    The connection pool is shared by every request, so connections and the cached OAuth
    token are reused instead of being re-created on each call.
    """
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            f"postgresql+psycopg://{USERNAME}:@{_resolve_host()}:{PORT}/{DATABASE}?sslmode=require",
            pool_recycle=1800,
        )
        event.listens_for(_engine.sync_engine, "do_connect")(_provide_token)
    return _engine


def _get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            bind=_get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _session_factory


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency: one session per request, commit on success, rollback on error."""
    async with _get_session_factory()() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def dispose_engine() -> None:
    """Close all pooled connections. Call on application shutdown."""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None
