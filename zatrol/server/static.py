from flask import Blueprint, render_template

blueprint = Blueprint("static", __name__, url_prefix="/")


@blueprint.route("/", defaults={"path": ""})
@blueprint.route("/<path>")
def serve(path):
    return render_template("index.html")
