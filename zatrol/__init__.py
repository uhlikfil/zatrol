import logging
import os
import sys

from flask import Flask

from zatrol import exception
from zatrol.config import Config
from zatrol.database import connection_manager
from zatrol.model import graphql_schema
from zatrol.riot import riot_api
from zatrol.services import champion as champion_svc
from zatrol.services import generate as generate_svc
from zatrol.services import match_history as match_history_svc


def init_logger(name: str, level=logging.WARN) -> None:
    logger = logging.getLogger(name)
    logger.handlers.clear()
    fmt = logging.Formatter("[%(asctime)s] [%(levelname)7s] [%(process)s %(thread)s]: %(message)s (%(filename)s:%(lineno)s)")  # fmt: skip
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)

    if level:
        logger.setLevel(level)
        ch.setLevel(level)

    logger.addHandler(ch)


def create_app() -> Flask:
    app = Flask(__name__.split(".")[0])

    if os.getenv("SERVE_UI") == "1":
        from zatrol.config import Config
        from zatrol.routes import static

        app.template_folder = Config.path.ui_build
        app.static_folder = app.template_folder + "/static"
        app.register_blueprint(static.blueprint)
    else:  # the UI will be running on a different port, CORS is needed
        from flask_cors import CORS

        CORS(app)

    for exc, handler in exception.handler_map.items():
        app.register_error_handler(exc, handler)

    _register_routes(app)

    return app


def _register_routes(app: Flask) -> None:
    from zatrol.routes import generate, graphql, metadata

    for route in (graphql, generate, metadata):
        app.register_blueprint(route.blueprint)


def init() -> None:
    try:
        init_logger("sqlalchemy.engine", logging.WARN)
        init_logger(__package__, logging.DEBUG)
        Config.load_env()
        for initable in (
            riot_api,
            connection_manager,
            generate_svc,
            champion_svc,
            match_history_svc,
        ):
            initable.init()
    except Exception as error:
        print(error, file=sys.stderr)
        sys.exit(1)


def wsgi():
    init()
    return create_app()
