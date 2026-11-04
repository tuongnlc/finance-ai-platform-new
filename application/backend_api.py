from contextlib import asynccontextmanager

from fastapi import FastAPI

from application.routes import newspaper_summary
from infrastructure.database.session import dispose_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await dispose_engine()


def create_chatbot_api():
    app = FastAPI(
        title="Chatbot API",
        version="1.0",
        description="API for chatbot",
        contact={"name": "Tuong Nguyen"},
        license_info={"name": "MIT License"},
        lifespan=lifespan,
    )
    app.include_router(newspaper_summary.router)

    return app


app = create_chatbot_api()
