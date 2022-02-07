from typing import Union

from zatrol.api import riot_api
from zatrol.database import connection_manager as cm
from zatrol.database import db_api
from zatrol.model.dbschema import Player
from zatrol.model.region import Region
from zatrol.services import match_history as match_history_svc


def insert_player(region: str, summoner_name: str) -> None:
    e_region = Region.parse(region)
    puuid = summoner_name_to_puuid(e_region, summoner_name)
    with cm.session_mkr() as sess:
        db_api.insert_player(sess, puuid, e_region, summoner_name)
        sess.commit()
    # match_history_svc.process_player(player)


def get_players() -> list[Player]:
    with cm.session_mkr() as sess:
        return db_api.select_all_players(sess)


def summoner_name_to_puuid(region: Union[str, Region], summoner_name: str) -> str:
    if isinstance(region, str):
        region = Region.parse(region)
    puuid = riot_api.get_puuid(region, summoner_name)
    if not puuid:
        raise ValueError(f"Player '{summoner_name}' not found in the {region} region")
    return puuid
