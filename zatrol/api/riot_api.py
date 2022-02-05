from riotwatcher import LolWatcher

from zatrol.config import Config

client: LolWatcher = None


def init() -> None:
    global client
    client = LolWatcher(Config.riot_api.api_key)


def fetch_champions() -> list[str]:
    versions = client.data_dragon.versions_for_region("eune")
    champions_version = versions["n"]["champion"]
    champ_list = client.data_dragon.champions(champions_version)
    return list(champ_list["data"].keys())
