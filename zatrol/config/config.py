import os
import pathlib

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class DbConnection:
    database_url: str


@dataclass(frozen=True)
class Riot:
    api_key: str
    champions_interval_h: float
    match_history_interval_h: float


@dataclass(frozen=True)
class Path:
    resources: pathlib.Path
    ui_build: str


class Config:
    """A class holding the app configuration - is loaded from environmental variables"""

    @classmethod
    def load_env(cls) -> None:
        try:
            cls.db_connection = DbConnection(
                os.getenv("DATABASE_URL"),
            )
            cls.riot = Riot(
                os.getenv("RIOT_API_KEY"),
                os.getenv("CHAMPIONS_INTERVAL_H"),
                os.getenv("MATCH_HISTORY_INTERVAL_H"),
            )
            cls.path = Path(
                os.getenv("RESOURCES_DIR"),
                os.getenv("UI_BUILD_DIR"),
            )
        except ValueError as error:
            raise ConfigLoadError(f"Error while loading configuration\n{error}")


class ConfigLoadError(Exception):
    pass
