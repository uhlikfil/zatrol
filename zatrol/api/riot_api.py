import requests
from riotwatcher import LolWatcher

from zatrol.config import Config

client: LolWatcher = None


def init() -> None:
    global client
    client = LolWatcher(Config.riot_api.api_key)


def fetch_champions() -> dict:
    champions_version = _version("champion")
    champ_list = client.data_dragon.champions(champions_version)
    return champ_list["data"]


def get_champion_icon(key: int) -> bytes:
    url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons"
    return requests.get(f"{url}/{key}.png").content


def _version(type_: str) -> str:
    versions = client.data_dragon.versions_for_region("eune")
    return versions["n"][type_]
