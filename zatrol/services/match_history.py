import threading
from logging import getLogger

from sqlalchemy.orm import Session

from zatrol.api import riot_api
from zatrol.config import Config
from zatrol.database import connection_manager as cm
from zatrol.database import db_api
from zatrol.model.dbschema import Summoner
from zatrol.services.img_gen import game_img
from zatrol.utils import threading_utils as tu

logger = getLogger(f"{__package__}.{__name__}")


def register() -> None:
    args = (Config.riot_api.match_history_interval_h * 60, _check_summoners)
    threading.Thread(target=tu.run_periodically, args=args).start()


def _check_summoners() -> None:
    logger.info("checking match history of all registered summoners")
    with cm.session_mkr() as sess:
        summoners = db_api.select_all_summoners(sess)
        logger.info("going to process history of all registered summoners")
        for summoner in summoners:
            process_summoner(sess, summoner)
        sess.commit()


def process_summoner(session: Session, summoner: Summoner) -> None:
    match_ids = riot_api.get_matches(summoner.region, summoner.puuid)
    if summoner.last_match:
        match_ids = list(filter(lambda m_id: m_id > summoner.last_match, match_ids))
    logger.info("found %d new matches for '%s'", len(match_ids), summoner.summoner_name)
    if not match_ids:
        return
    for m_id in match_ids:
        match_data = riot_api.get_match(summoner.region, m_id)["info"]
        _process_match(session, match_data, summoner.puuid)
    db_api.update_summoner_last_match(session, summoner.puuid, match_ids[0])


def _process_match(session: Session, data: dict, puuid: str) -> None:
    for participant in data["participants"]:
        if participant["puuid"] == puuid:
            break
    kills = participant["kills"]
    deaths = participant["deaths"]
    assists = participant["assists"]
    if deaths == 0 or _weighted_kda(kills, deaths, assists) >= 1:
        return None
    logger.info("found a nice game played as %s with %d/%d/%d", participant["championName"], kills, deaths, assists)  # fmt: skip
    img = game_img.create_img(
        participant["championId"],
        kills,
        deaths,
        assists,
        participant["win"],
    )
    db_api.insert_game(session, puuid, img, participant["championName"])


def _weighted_kda(k: int, d: int, a: int) -> float:
    return (3 * k + a) / (3 * d)
