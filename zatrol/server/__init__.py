import os

from flask import Flask

from zatrol.server import metadata


def create_app() -> Flask:
    app = Flask(__name__.split(".")[0])

    if os.getenv("SERVE_UI"):
        from zatrol.server import static

        app.template_folder = "/zatrol-ui/build"
        app.static_folder = "/zatrol-ui/build/static"
        app.register_blueprint(static.blueprint)

    else:  # the UI will be running on a different port, CORS is needed
        from flask_cors import CORS

        CORS(app)

    _register_err_handlers(app)
    _register_blueprints(app)

    return app


def _register_err_handlers(app: Flask) -> None:
    from zatrol.server import error_handlers

    app.register_error_handler(ValueError, error_handlers.unprocessable_entity)
    app.register_error_handler(KeyError, error_handlers.bad_request)
    app.register_error_handler(FileNotFoundError, error_handlers.not_found)


def _register_blueprints(app: Flask) -> None:
    from zatrol.server import generate, quote, summoner

    app.register_blueprint(generate.blueprint)
    app.register_blueprint(quote.blueprint)
    app.register_blueprint(metadata.blueprint)
    app.register_blueprint(summoner.blueprint)
