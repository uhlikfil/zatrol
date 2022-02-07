from http import HTTPStatus


def unprocessable_entity(exception) -> tuple[str, int]:
    return str(exception), HTTPStatus.UNPROCESSABLE_ENTITY


def bad_request(exception) -> tuple[str, int]:
    return "Invalid json body", HTTPStatus.BAD_REQUEST


def not_found(exception) -> tuple[str, int]:
    return str(exception), HTTPStatus.NOT_FOUND
