import requests
from requests.exceptions import HTTPError
from riotwatcher import LolWatcher

from zatrol.config import Config
from zatrol.model.region import Region

client: LolWatcher = None


def init() -> None:
    global client
    client = LolWatcher(Config.riot_api.api_key)


def get_puuid(region: Region, summoner_name: str) -> str:
    try:
        return client.summoner.by_name(region.value, summoner_name)["puuid"]
    except HTTPError:
        return None


def get_matches(region: Region, puuid: str, after_time: int) -> list[dict]:
    return client.match.matchlist_by_puuid(region.value, puuid, start=after_time)


def get_match(region: Region, match_id: str) -> dict:
    return client.match.by_id(region.value, match_id)


def get_champions() -> dict:
    champions_version = _version("champion")
    champ_list = client.data_dragon.champions(champions_version)
    return champ_list["data"]


def get_champion_icon(key: int) -> bytes:
    url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons"
    return requests.get(f"{url}/{key}.png").content


def _version(type_: str) -> str:
    versions = client.data_dragon.versions_for_region("eune")
    return versions["n"][type_]
