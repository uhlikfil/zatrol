from http import HTTPStatus

from flask import Blueprint, jsonify, request

from zatrol.services import generate as generate_svc

blueprint = Blueprint("generate", __name__, url_prefix="/api/generate")


@blueprint.get("/<puuid>")
def get(puuid):
    return {"image": generate_svc.generate(puuid)}, HTTPStatus.OK
