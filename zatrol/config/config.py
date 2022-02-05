import os

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class DbConnection:
    host: str
    port: int
    username: str
    password: str
    database: str


@dataclass(frozen=True)
class Server:
    port: int


@dataclass(frozen=True)
class RiotAPI:
    api_key: str
    champ_fetch_interval_h: int


class Config:
    """a class holding the app configuration - is loaded from environmental variables"""

    @classmethod
    def load_env(cls) -> None:
        try:
            cls.db_connection = DbConnection(
                os.getenv("DB_HOST"),
                os.getenv("DB_PORT"),
                os.getenv("DB_USR"),
                os.getenv("DB_PSW"),
                os.getenv("DATABASE"),
            )
            cls.server = Server(os.getenv("SERVER_PORT"))
            cls.riot_api = RiotAPI(
                os.getenv("RIOT_API_KEY"), os.getenv("CHAMP_FETCH_INTERVAL_H")
            )
        except ValueError as error:
            raise ConfigLoadError(f"Error while loading configuration\n{error}")


class ConfigLoadError(Exception):
    pass
