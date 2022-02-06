from zatrol.database import connection_manager as cm
from zatrol.database import db_api
from zatrol.model.dbschema import Quote
from zatrol.services import champions as champ_list_svc


def insert_quote(text: str, champ_restrictions: list[str]) -> None:
    if not 3 <= len(text) < 256:
        raise ValueError(f"Incorrect quote length {len(text)}")
    champions = champ_list_svc.validate_champions(champ_restrictions)
    with cm.session_mkr() as sess:
        db_api.insert_quote(sess, text, champions)
        sess.commit()


def get_random_quote() -> Quote:
    with cm.session_mkr() as sess:
        return db_api.select_random_quote(sess)
