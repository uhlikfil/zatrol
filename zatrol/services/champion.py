from logging import getLogger

from zatrol.config import Config
from zatrol.riot import riot_api
from zatrol.utils import threading_utils as tu

logger = getLogger(f"{__package__}.{__name__}")

champions = dict()


def init() -> None:
    interval_minutes = Config.riot.champions_interval_h * 60
    tu.run_periodically(interval_minutes, _update_champions)


def get_champions() -> list[str]:
    return list(sorted(map(lambda c: c["name"], champions.values())))


def validate_champions(champ_names: list[str]) -> list[str]:
    valid_names = []
    invalid_names = []
    for name in champ_names:
        champion = champions.get(name.lower())
        if champion:
            valid_names.append(champion["name"])
        else:
            invalid_names.append(name)
    if invalid_names:
        raise ValueError(f"Invalid champion names: {invalid_names}")
    return valid_names


def _update_champions() -> None:
    global champions
    logger.info("updating champion list")
    champs = riot_api.get_champions()
    logger.info("got %d champions from Riot API", len(champs))
    champions = {name.lower(): data for name, data in champs.items()}
