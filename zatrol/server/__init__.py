from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__.split(".")[0])

    _register_err_handlers(app)
    _register_blueprints(app)

    return app


def _register_err_handlers(app: Flask) -> None:
    from zatrol.server import error_handlers

    app.register_error_handler(ValueError, error_handlers.unprocessable_entity)
    app.register_error_handler(KeyError, error_handlers.bad_request)
    app.register_error_handler(FileNotFoundError, error_handlers.not_found)


def _register_blueprints(app: Flask) -> None:
    from zatrol.server import generate, player, quote

    app.register_blueprint(generate.blueprint)
    app.register_blueprint(player.blueprint)
    app.register_blueprint(quote.blueprint)
