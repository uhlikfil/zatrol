from http import HTTPStatus

from flask import Blueprint, jsonify, request

from zatrol.services import summoner as summoner_svc

blueprint = Blueprint("summoner", __name__, url_prefix="/api/summoner")


@blueprint.get("")
def get():
    result = summoner_svc.get_summoners()
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
    summoner_svc.insert_summoner(body["region"], body["summoner_name"])
    return "", HTTPStatus.NO_CONTENT
