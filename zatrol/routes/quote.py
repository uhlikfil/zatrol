from http import HTTPStatus

import flask_pydantic
from flask import Blueprint

from zatrol.exception import NotFound
from zatrol.model.api_schema import Quote
from zatrol.services import quote as quotes_svc

blueprint = Blueprint("quote", __name__, url_prefix="/api/quote")


@blueprint.get("/<puuid>")
@flask_pydantic.validate(response_many=True)
def get(puuid):
    quotes = quotes_svc.get_quotes(puuid)
    if not quotes:
        raise NotFound(f"No quotes for a summoner puuid '{puuid}'")
    return [Quote(**quote) for quote in quotes]


@blueprint.post("")
@flask_pydantic.validate()
def post(body: Quote):
    restrictions = body.champ_restrictions if body.champ_restrictions else []
    quotes_svc.add_quote(body.puuid, body.text, restrictions)
    return "", HTTPStatus.NO_CONTENT
