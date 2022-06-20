from zatrol.exception import error_handlers
from zatrol.exception.exception import NotFound

handler_map = {
    NotFound: error_handlers.not_found,
}
