import threading
from logging import getLogger

from zatrol.api import riot_api
from zatrol.config import Config
from zatrol.database import connection_manager as cm
from zatrol.database import db_api
from zatrol.model.region import Region

logger = getLogger(f"{__package__}.{__name__}")


def check_history(region: Region, player_puuid: str, after_time: int) -> None:
    match_ids = riot_api.get_matches(region.value, player_puuid, after_time)
    for m_id in match_ids:
        match = riot_api.get_match(region, m_id)

    print()


def register() -> None:
    _check_players()


def _check_players() -> None:
    logger.info("checking match history of all registered players")
    with cm.session_mkr() as sess:
        players = db_api.select_all_players(sess)
    logger.info("going to update %d players", len(players))
    champions = {name.lower(): data for name, data in champs.items()}
    interval_s = 60 * 60 * Config.riot_api.champ_fetch_interval_h
    logger.info("will fetch again in %s seconds", interval_s)
    threading.Timer(interval_s, _update_database).start()
