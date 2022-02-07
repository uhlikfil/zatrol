import threading
from logging import getLogger

from zatrol.api import riot_api
from zatrol.config import Config
from zatrol.database import connection_manager as cm
from zatrol.database import db_api
from zatrol.model.dbschema import Player
from zatrol.services import game_img
from zatrol.utils import threading_utils

logger = getLogger(f"{__package__}.{__name__}")


def register() -> None:
    threading.Thread(target=_check_players).start()


def _check_players() -> None:
    logger.info("checking match history of all registered players")
    with cm.session_mkr() as sess:
        players = db_api.select_all_players(sess)
    logger.info("going to process history of %d players", len(players))
    for player in players:
        process_player(player)

    threading_utils.schedule(_check_players, Config.riot_api.match_history_interval_h)


def process_player(player: Player) -> None:
    match_ids = riot_api.get_matches(player.region, player.puuid)
    if player.last_match:
        match_ids = list(filter(lambda m_id: m_id > player.last_match, match_ids))
    logger.info("found %d new matches for '%s'", len(match_ids), player.summoner_name)
    if not match_ids:
        return
    for m_id in match_ids:
        match_data = riot_api.get_match(player.region, m_id)["info"]
        _process_match(match_data, player.puuid)
    with cm.session_mkr() as sess:
        db_api.update_player_last_match(sess, player.puuid, match_ids[0])
        sess.commit()


def _process_match(data: dict, puuid: str) -> None:
    for participant in data["participants"]:
        if participant["puuid"] == puuid:
            break
    kills = participant["kills"]
    deaths = participant["deaths"]
    assists = participant["assists"]
    if deaths == 0 or _weighted_kda(kills, deaths, assists) >= 1:
        return None

    img = game_img.create_img(
        participant["championId"],
        kills,
        deaths,
        assists,
        participant["win"],
    )
    with cm.session_mkr() as sess:
        db_api.insert_game(sess, puuid, img, participant["championName"])
        sess.commit()


def _weighted_kda(k: int, d: int, a: int) -> float:
    return (3 * k + a) / 3 * d
