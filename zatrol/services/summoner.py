import threading
from typing import Union

from sa_decor import with_connection

from zatrol.database import db_api
from zatrol.model.db_schema import Summoner
from zatrol.model.region import Region
from zatrol.riot import riot_api
from zatrol.services import match_history as match_history_svc


@with_connection()
def insert_summoner(region: str, summoner_name: str, *, connection) -> None:
    @with_connection()
    def process_new(*, connection):
        summoner = db_api.select_summoner(connection, puuid)
        match_history_svc.process_summoner(connection, summoner)

    e_region = Region.parse(region)
    puuid = summoner_name_to_puuid(e_region, summoner_name)
    db_api.insert_summoner(connection, puuid, e_region, summoner_name)

    threading.Thread(target=process_new).start()


@with_connection()
def get_summoners(*, connection) -> list[Summoner]:
    return list(db_api.select_all_summoners(connection))


def summoner_name_to_puuid(region: Union[str, Region], summoner_name: str) -> str:
    if isinstance(region, str):
        region = Region.parse(region)
    puuid = riot_api.get_puuid(region, summoner_name)
    if not puuid:
        msg = f"Summoner '{summoner_name}' not found in the {region.name} region"
        raise ValueError(msg)
    return puuid
