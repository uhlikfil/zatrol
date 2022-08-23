import logging

from fastapi import FastAPI
from fastapi_restful.tasks import repeat_every

from zatrol.exceptions import InvalidValue
from zatrol.services import riot_client
from zatrol.settings import Settings

logger = logging.getLogger(f"{__package__}.{__name__}")

champions = dict()


def init(app: FastAPI) -> None:
    interval_sec = Settings.const.CHAMPS_INTERVAL_H * 60 * 60

    @repeat_every(seconds=interval_sec)
    def update_champions() -> None:
        global champions
        logger.info("updating champion list")
        champs = riot_client.get_champions()
        logger.info("got %d champions from Riot API", len(champs))
        champions = {name.lower(): data for name, data in champs.items()}

    app.add_event_handler("startup", update_champions)


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
        raise InvalidValue(f"Invalid champion names: {invalid_names}")
    return valid_names
