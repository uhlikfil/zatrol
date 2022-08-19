from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class InvalidValue(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class NotFound(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, detail)


class AlreadyExists(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail)


async def handle_validation_error(_, exc: RequestValidationError):
    msg = "\n".join(map(_parse_err, exc.errors()))
    return JSONResponse({"detail": msg}, status.HTTP_422_UNPROCESSABLE_ENTITY)


def _parse_err(err) -> str:
    return f'{err["loc"][1].capitalize()}: {err["msg"].capitalize()}'
