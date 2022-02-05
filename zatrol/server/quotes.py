from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from zatrol.services import quotes as quotes_svc

blueprint = Blueprint("quote", __name__, url_prefix="/api/quote")


@blueprint.get("")
def get():
    resp = quotes_svc.get_random_quote()
    return jsonify(resp), HTTPStatus.OK


@blueprint.post("")
def post():
    body = request.json
    if not body or not body["text"] or not body["champ_restrictions"]:
        abort(HTTPStatus.BAD_REQUEST, description="Invalid json body")
    try:
        resp = quotes_svc.insert_quote(body["text"], body["champs"])
        return jsonify(resp), HTTPStatus.OK
    except ValueError as err:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, description=str(err))
