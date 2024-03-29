import logging
import os

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi_restful.timing import add_timing_middleware

from zatrol import exceptions as exc
from zatrol.database import connection as db_connection
from zatrol.model.api_schema import ErrorDTO
from zatrol.routes import generate, metadata, quote, summoner
from zatrol.services import champion as champ_svc
from zatrol.services import match_history as match_history_svc
from zatrol.services import riot_client
from zatrol.settings import Settings

logger = logging.getLogger("uvicorn")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Zatrol",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        responses={status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ErrorDTO}},
    )

    add_timing_middleware(app, logger.info)
    app.add_event_handler("startup", init_logging)
    app.add_exception_handler(RequestValidationError, exc.handle_validation_error)

    # order matters
    for initable in (db_connection, riot_client, champ_svc, match_history_svc):
        initable.init(app)

    for route in (metadata, quote, summoner, generate):
        app.include_router(route.router, prefix="/api")

    if Settings.config.SERVE_UI:
        from fastapi.staticfiles import StaticFiles

        from zatrol.routes import static

        static_files = StaticFiles(directory=Settings.path.UI_BUILD)
        app.include_router(static.router)
        app.mount("/", static_files, name="UI static files")
    else:  # the UI will be running on a different port, CORS is needed
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    return app


def init_logging() -> None:
    root_logger = logging.getLogger(__package__)
    root_logger.setLevel(logger.level)

    for handler in logger.handlers:
        root_logger.addHandler(handler)
