import logging
import os

from fastapi import FastAPI
from fastapi_restful.timing import add_timing_middleware

logger = logging.getLogger("uvicorn")


def create_app() -> FastAPI:
    app = FastAPI(title="Zatrol", docs_url="/api/docs")

    if os.getenv("SERVE_UI"):
        from zatrol.routes import static

        # TODO
    else:  # the UI will be running on a different port, CORS is needed
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    add_timing_middleware(app, logger.info)
    app.add_event_handler("startup", init_logging)
    init_app(app)
    init_routes(app)

    return app


def init_logging() -> None:
    root_logger = logging.getLogger(__package__)
    root_logger.setLevel(logger.level)

    for handler in logger.handlers:
        root_logger.addHandler(handler)


def init_app(app: FastAPI) -> None:
    from zatrol.database import connection as db_connection
    from zatrol.services import champion as champ_svc
    from zatrol.services import riot_client

    # order matters
    for initable in (db_connection, riot_client, champ_svc):
        initable.init(app)


def init_routes(app: FastAPI) -> None:
    from zatrol.routes import metadata, quote, summoner

    for route in (metadata, quote, summoner):
        app.include_router(route.router)
