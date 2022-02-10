import requests
from requests.exceptions import HTTPError
from riotwatcher import LolWatcher

from zatrol.config import Config
from zatrol.model.region import Region, RegionArea

client: LolWatcher = None


def init() -> None:
    global client
    client = LolWatcher(Config.riot_api.api_key)


def get_puuid(region: Region, summoner_name: str) -> str:
    try:
        return client.summoner.by_name(region.value, summoner_name)["puuid"]
    except HTTPError:
        return None


def get_matches(region: Region, puuid: str) -> list[str]:
    area = RegionArea.get_area(region)
    return client.match.matchlist_by_puuid(area.value, puuid)


def get_match(region: Region, match_id: str) -> dict:
    area = RegionArea.get_area(region)
    return client.match.by_id(area.value, match_id)


def get_champions() -> dict:
    champions_version = _version("champion")
    champ_list = client.data_dragon.champions(champions_version)
    return champ_list["data"]


def get_champion_icon(champion_name: int) -> bytes:
    url = "http://ddragon.leagueoflegends.com/cdn/12.3.1/img/champion"
    return requests.get(f"{url}/{champion_name}.png").content


def _version(type_: str) -> str:
    versions = client.data_dragon.versions_for_region("eune")
    return versions["n"][type_]
