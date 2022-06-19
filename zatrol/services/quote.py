from sa_decor import with_connection
from sqlalchemy.exc import IntegrityError

from zatrol.database import db_api
from zatrol.exception import UnregisteredSummoner
from zatrol.model.db_schema import Quote
from zatrol.services import champion as champion_svc


@with_connection()
def get_quotes(puuid: str, *, connection) -> list[Quote]:
    return db_api.select_quotes(connection, puuid)


@with_connection()
def add_quote(
    puuid: str, text: str, champ_restrictions: list[str], *, connection
) -> None:
    champions = champion_svc.validate_champions(champ_restrictions)
    try:
        db_api.insert_quote(connection, puuid, text, champions)
    except IntegrityError:
        raise UnregisteredSummoner(puuid)
