from flask import Flask


def create_app():
    from zatrol.server.quotes import blueprint as quotes_bp

    app = Flask(__name__.split(".")[0])
    app.register_blueprint(quotes_bp)
    return app
