import threading
from logging import getLogger

from zatrol.api import riot_api
from zatrol.config import Config

logger = getLogger(f"{__package__}.{__name__}")

champions = dict()


def validate_champions(champ_names: list[str]) -> list[str]:
    valid_names = []
    invalid_names = []
    for name in champ_names:
        valid_name = champions.get(name.lower())
        if valid_name:
            valid_names.append(valid_name["name"])
        else:
            invalid_names.append(name)
    if invalid_names:
        raise ValueError(f"Invalid champion names: {invalid_names}")
    return valid_names


def register() -> None:
    _update_database()


def _update_database() -> None:
    global champions
    logger.info("updating champion list in the database")
    champs = riot_api.get_champions()
    logger.info("got %d champions from Riot API", len(champs))
    champions = {name.lower(): data for name, data in champs.items()}
    interval_s = 60 * 60 * Config.riot_api.champ_fetch_interval_h
    logger.info("will fetch again in %d seconds", interval_s)
    threading.Timer(interval_s, _update_database).start()
