from zatrol.config import Config
from zatrol.database import connection_manager as cm
from zatrol.database import db_api
from zatrol.services import champion as champion_svc


def insert_quote(puuid: str, text: str, champ_restrictions: list[str]) -> None:
    if not Config.services.min_quote_len <= len(text) < Config.services.max_quote_len:
        raise ValueError(f"Quote length must be between {Config.services.min_quote_len} and {Config.services.max_quote_len} characters")  # fmt: skip
    champions = champion_svc.validate_champions(champ_restrictions)
    try:
        with cm.session_mkr() as sess:
            db_api.insert_quote(sess, puuid, text, champions)
            sess.commit()
    except:
        raise ValueError("Attempted to add quote to a unregistered summoner")
