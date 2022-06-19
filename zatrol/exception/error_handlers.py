from http import HTTPStatus


def _err(msg):
    return {"error": str(msg)}


def unprocessable_entity(exception) -> tuple[str, int]:
    return _err(exception), HTTPStatus.UNPROCESSABLE_ENTITY


def bad_request(_) -> tuple[str, int]:
    return _err("Invalid json body"), HTTPStatus.BAD_REQUEST


def not_found(exception) -> tuple[str, int]:
    return _err(exception), HTTPStatus.NOT_FOUND


def unregistered_summoner(puuid: str) -> tuple[str, int]:
    return (
        _err(f"The summoner '{puuid}' has not been registered in the application."),
        HTTPStatus.NOT_FOUND,
    )
