from sqlalchemy.exc import IntegrityError

from zatrol.database import connection_manager as cm
from zatrol.database import db_api
from zatrol.model.dbschema import Quote
from zatrol.services import champions as champ_list_svc


def insert_quote(puuid: str, text: str, champ_restrictions: list[str]) -> None:
    if not 3 <= len(text) < 64:
        raise ValueError(f"Incorrect quote length {len(text)}")
    champions = champ_list_svc.validate_champions(champ_restrictions)
    try:
        with cm.session_mkr() as sess:
            db_api.insert_quote(sess, puuid, text, champions)
            sess.commit()
    except:
        raise ValueError("Attempted to add quote to a unregistered player")
