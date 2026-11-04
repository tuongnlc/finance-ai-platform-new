from databricks.sdk import WorkspaceClient
import asyncio
import time

from dotenv import load_dotenv
import os

from sqlalchemy import text, event
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

w = WorkspaceClient()


DATABRICKS_ENDPOINT = os.getenv("DATABRICKS_ENDPOINT")
# Configure connection parameters (get these from the Connect dialog in the Lakebase App)
endpoint = os.getenv("LAKE_FLOW_ENDPOINT")

username = os.getenv("PGUSER")  # Your DB identity
# The Postgres host comes from the Lakebase compute endpoint, not the workspace host
endpoint_info = w.postgres.get_endpoint(name=endpoint)
host = endpoint_info.status.hosts.host  # Your compute endpoint hostname
port = 5432
database = "databricks_postgres"

# Create async SQLAlchemy engine (psycopg v3 supports async natively)
connection_pool = create_async_engine(f"postgresql+psycopg://{username}:@{host}:{port}/{database}?sslmode=require")

# Global variables for token management
postgres_password = None
token_expiry = 0.0  # Unix timestamp when the current token expires

@event.listens_for(connection_pool.sync_engine, "do_connect")
def provide_token(dialect, conn_rec, cargs, cparams):
    global postgres_password, token_expiry

    # Refresh token if None or expiring within 2 minutes
    if postgres_password is None or time.time() >= token_expiry - 120:
        print("Refreshing PostgreSQL OAuth token")
        credential = w.postgres.generate_database_credential(endpoint=endpoint)
        postgres_password = credential.token
        token_expiry = credential.expire_time.seconds

    cparams["password"] = postgres_password


async def main() -> None:
    # Use the connection pool
    async with connection_pool.connect() as conn:
        result = await conn.execute(text("SELECT version()"))
        for row in result:
            print(f"Connected to PostgreSQL database. Version: {row}")
    await connection_pool.dispose()


asyncio.run(main())
