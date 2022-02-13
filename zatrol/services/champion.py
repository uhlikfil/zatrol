from logging import getLogger

from zatrol.api import riot_api
from zatrol.config import Config
from zatrol.utils import threading_utils as tu

logger = getLogger(f"{__package__}.{__name__}")

champions = dict()


def get_champions() -> list[str]:
    names = [champion["name"] for champion in champions.values()]
    return list(sorted(names))


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


def register() -> None:
    interval_minutes = Config.riot_api.champions_interval_h * 60
    tu.run_periodically(interval_minutes, _update_champions)


def _update_champions() -> None:
    global champions
    logger.info("updating champion list in the database")
    champs = riot_api.get_champions()
    logger.info("got %d champions from Riot API", len(champs))
    champions = {name.lower(): data for name, data in champs.items()}
