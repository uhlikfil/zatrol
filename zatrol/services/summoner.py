import threading

from sa_decor import with_connection

from zatrol.database import db_api
from zatrol.exception import NotFound
from zatrol.model.region import Region
from zatrol.riot import riot_api
from zatrol.services import match_history as match_history_svc


@with_connection()
def insert_summoner(region: Region, summoner_name: str, *, connection) -> None:
    @with_connection()
    def process_new(*, connection):
        summoner = db_api.select_summoner(connection, puuid)
        match_history_svc.process_summoner(summoner, connection=connection)

    puuid = _summoner_name_to_puuid(region, summoner_name)
    db_api.insert_summoner(connection, puuid, region, summoner_name)

    threading.Thread(target=process_new).start()


def _summoner_name_to_puuid(region: Region, summoner_name: str) -> str:
    puuid = riot_api.get_puuid(region, summoner_name)
    if not puuid:
        msg = f"Summoner '{summoner_name}' not found in the {region.name} region"
        raise NotFound(msg)
    return puuid
