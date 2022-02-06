from flask import Flask


def create_app():
    app = Flask(__name__.split(".")[0])

    _register_err_handlers(app)
    _register_blueprints(app)

    return app


def _register_err_handlers(app: Flask) -> None:
    from zatrol.server import error_handlers

    app.register_error_handler(ValueError, error_handlers.unprocessable_entity)
    app.register_error_handler(KeyError, error_handlers.bad_request)


def _register_blueprints(app: Flask) -> None:
    from zatrol.server import player, quote

    app.register_blueprint(quote.blueprint)
    app.register_blueprint(player.blueprint)
