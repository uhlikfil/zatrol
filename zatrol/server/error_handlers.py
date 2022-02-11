from http import HTTPStatus


def _err(msg):
    return {"error": str(msg)}


def unprocessable_entity(exception) -> tuple[str, int]:
    return _err(exception), HTTPStatus.UNPROCESSABLE_ENTITY


def bad_request(_) -> tuple[str, int]:
    return _err("Invalid json body"), HTTPStatus.BAD_REQUEST


def not_found(exception) -> tuple[str, int]:
    return _err(exception), HTTPStatus.NOT_FOUND
