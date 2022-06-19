from zatrol.exception import error_handlers
from zatrol.exception.exception import NotFound, UnregisteredSummoner

handler_map = {
    ValueError: error_handlers.unprocessable_entity,
    KeyError: error_handlers.bad_request,
    NotFound: error_handlers.not_found,
    UnregisteredSummoner: error_handlers.unregistered_summoner,
}
