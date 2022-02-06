from http import HTTPStatus


def unprocessable_entity(exception):
    return str(exception), HTTPStatus.UNPROCESSABLE_ENTITY


def bad_request(exception):
    return "Invalid json body", HTTPStatus.BAD_REQUEST


def not_found(exception):
    return str(exception), HTTPStatus.NOT_FOUND
