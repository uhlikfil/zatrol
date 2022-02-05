import threading
from logging import getLogger

from riotwatcher import LolWatcher

from zatrol.config import Config
from zatrol.database import connection_manager as cm
from zatrol.database import db_api

logger = getLogger(f"{__package__}.{__name__}")

client: LolWatcher = None


def register() -> None:
    global client
    client = LolWatcher(Config.riot_api.api_key)

    threading.Thread(target=_update_database).start()


def _update_database() -> None:
    logger.info("updating champion list in the database")
    versions = client.data_dragon.versions_for_region("eune")
    champions_version = versions["n"]["champion"]
    champ_list: dict = client.data_dragon.champions(champions_version)
    names = champ_list["data"].keys()
    logger.info("got %s champions from Riot API", len(names))
    with cm.session_mkr() as sess:
        db_api.insert_champions(sess, names)
        sess.commit()
    # run again tomorrow
    threading.Timer(60 * 60 * 24, _update_database).start()
