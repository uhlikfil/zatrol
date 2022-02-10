from http import HTTPStatus

from flask import Blueprint, jsonify, request

from zatrol.model.region import Region

blueprint = Blueprint("region", __name__, url_prefix="/api/region")


@blueprint.get("")
def get():
    resp = [reg.name for reg in Region]
    return jsonify(resp), HTTPStatus.OK
