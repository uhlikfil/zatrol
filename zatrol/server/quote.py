from http import HTTPStatus

from flask import Blueprint, request

from zatrol.database import connection_manager as cm
from zatrol.database import db_api
from zatrol.services import quote as quotes_svc

blueprint = Blueprint("quote", __name__, url_prefix="/api/quote")


@blueprint.get("/<puuid>")
def get(puuid):
    with cm.session_mkr() as sess:
        result = db_api.select_random_quote(sess, puuid)
    if not result:
        raise FileNotFoundError(f"No quotes for a player puuid '{puuid}'")
    resp = {"text": result.text, "champ_restrictions": result.champ_restrictions}
    return resp, HTTPStatus.OK


@blueprint.post("")
def post():
    body = request.json
    if not body or "puuid" not in body or "text" not in body:
        raise KeyError
    restrictions = body.get("champ_restrictions", [])
    quotes_svc.insert_quote(body["puuid"], body["text"], restrictions)
    return "", HTTPStatus.NO_CONTENT
