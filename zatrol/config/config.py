import os

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class DbConnection:
    database_url: str


@dataclass(frozen=True)
class RiotAPI:
    api_key: str
    champions_interval_h: float
    match_history_interval_h: float


@dataclass(frozen=True)
class Services:
    assets_dir: str
    min_quote_len: int
    max_quote_len: int


class Config:
    """a class holding the app configuration - is loaded from environmental variables"""

    @classmethod
    def load_env(cls) -> None:
        try:
            cls.db_connection = DbConnection(os.getenv("DATABASE_URL"))
            cls.riot_api = RiotAPI(
                os.getenv("RIOT_API_KEY"),
                os.getenv("CHAMPIONS_INTERVAL_H"),
                os.getenv("MATCH_HISTORY_INTERVAL_H"),
            )
            cls.services = Services(os.getenv("ASSETS_DIR"), 3, 100)
        except ValueError as error:
            raise ConfigLoadError(f"Error while loading configuration\n{error}")


class ConfigLoadError(Exception):
    pass
