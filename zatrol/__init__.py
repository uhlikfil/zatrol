import logging
import sys

from zatrol.api import riot_api
from zatrol.config import Config
from zatrol.database import connection_manager
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


def init() -> None:
    try:
        init_logger("sqlalchemy.engine", logging.WARN)
        init_logger(__package__, logging.DEBUG)
        Config.load_env()
        riot_api.init()
        connection_manager.init()
        generate_svc.init()
        champion_svc.register()
        match_history_svc.register()
    except Exception as error:
        print(error, file=sys.stderr)
        sys.exit(1)


def wsgi():
    from zatrol.server import create_app

    init()
    app = create_app()
    validate(app)
    return app


def validate(app) -> None:
    from pathlib import Path

    print(app.template_folder)
    print(app.static_folder)
    print(list(Path(app.template_folder).glob("*")))
