from http import HTTPStatus

from flask import Blueprint, jsonify, request

from zatrol.services import player as player_svc

blueprint = Blueprint("player", __name__, url_prefix="/api/player")


@blueprint.get("")
def get():
    result = player_svc.get_players()
    resp = [
        {
            "puuid": p.puuid,
            "region": p.region.name,
            "summoner_name": p.summoner_name,
            "last_match": p.last_match,
        }
        for p in result
    ]
    return jsonify(resp), HTTPStatus.OK


@blueprint.post("")
def post():
    body = request.json
    if not body or "region" not in body or "summoner_name" not in body:
        raise KeyError
    player_svc.insert_player(body["region"], body["summoner_name"])
    return "", HTTPStatus.NO_CONTENT
