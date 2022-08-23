from logging import getLogger

from fastapi import FastAPI
from fastapi_restful.tasks import repeat_every

from zatrol.database.dao.game import GameDAO
from zatrol.database.dao.summoner import SummonerDAO
from zatrol.database.schema import Summoner
from zatrol.services import riot_client
from zatrol.services.img_gen import game_img
from zatrol.settings import Settings

logger = getLogger(f"{__package__}.{__name__}")


def init(app: FastAPI) -> None:
    interval_sec = Settings.const.HISTORY_INTERVAL_H * 60 * 60

    @repeat_every(seconds=interval_sec)
    async def check_summoners() -> None:
        async with app.state.db_engine.begin() as connection:
            summoner_dao = SummonerDAO(connection)
            game_dao = GameDAO(connection)
            summoners = await summoner_dao.get_all()
            logger.info("going to process history of all registered summoners")
            for summoner in summoners:
                await process_summoner(summoner_dao, game_dao, summoner)
            logger.info("all registered summoners processed")

    app.add_event_handler("startup", check_summoners)


async def process_summoner(
    summoner_dao: SummonerDAO, game_dao: GameDAO, summoner: Summoner
) -> None:
    match_ids = riot_client.get_matches(summoner.region, summoner.puuid)
    if summoner.last_match:
        match_ids = list(filter(lambda m_id: m_id > summoner.last_match, match_ids))
    logger.info("found %d new matches for '%s'", len(match_ids), summoner.summoner_name)
    if not match_ids:
        return
    for m_id in match_ids:
        match_data = riot_client.get_match(summoner.region, m_id)["info"]
        await _process_match(game_dao, match_data, summoner.puuid)
    await summoner_dao.update(summoner.puuid, last_match=match_ids[0])


async def _process_match(dao: GameDAO, data: dict, puuid: str) -> None:
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
    await dao.create(puuid, img, participant["championName"])


def _weighted_kda(k: int, d: int, a: int) -> float:
    return (3 * k + a) / (3 * d)
