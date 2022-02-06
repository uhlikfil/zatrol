from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from zatrol.services import quotes as quotes_svc

blueprint = Blueprint("quote", __name__, url_prefix="/api/quote")


@blueprint.get("")
def get():
    result = quotes_svc.get_random_quote()
    if not result:
        return None
    resp = {"text": result.text, "champ_restrictions": result.champ_restrictions}
    return jsonify(resp), HTTPStatus.OK


@blueprint.post("")
def post():
    body = request.json
    if not body or not body["text"]:
        abort(HTTPStatus.BAD_REQUEST, description="Invalid json body")
    try:
        quotes_svc.insert_quote(body["text"], body.get("champ_restrictions", []))
        return "", HTTPStatus.NO_CONTENT
    except ValueError as err:
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, description=str(err))
