from http import HTTPStatus

from flask import Blueprint, jsonify

from zatrol.model.region import Region
from zatrol.services import champion as champion_svc

blueprint = Blueprint("metadata", __name__, url_prefix="/api/metadata")


@blueprint.get("/region")
def get_region():
    resp = [reg.name for reg in Region]
    return jsonify(resp), HTTPStatus.OK


@blueprint.get("/champion")
def get_champion():
    return jsonify(champion_svc.get_champions()), HTTPStatus.OK
