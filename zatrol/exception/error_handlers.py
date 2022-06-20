from functools import wraps
from http import HTTPStatus

from zatrol.model import graphql_schema


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


def mutate_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = graphql_schema.MutationResult(ok=True)
        try:
            func(*args, **kwargs)
        except Exception as error:
            result.ok = False
            result.error = str(error)
        return args[1].return_type.graphene_type(result=result)

    return wrapper
