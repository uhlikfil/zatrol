from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio.engine import AsyncConnection, create_async_engine
from starlette.requests import Request

from zatrol.settings import Settings


def init(app: FastAPI) -> None:
    async def init_db():
        engine = create_async_engine(Settings.db.DB_URI, future=True)
        app.state.db_engine = engine

    app.add_event_handler("startup", init_db)


async def get_connection(request: Request) -> AsyncGenerator[AsyncConnection, None]:
    """
    Create and get database connection.

    :param request: current request.
    :yield: database connection.
    """

    async with request.app.state.db_engine.begin() as connection:
        yield connection
