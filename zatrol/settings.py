import pathlib

from pydantic.env_settings import BaseSettings


class Database(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "zatrol"
    DB_USER: str = "postgres"
    DB_PASS: str = "root"

    @property
    def DB_URI(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Const(BaseSettings):
    CHAMPS_INTERVAL_H: float = 0.1
    HISTORY_INTERVAL_H: float = 0.1
    MIN_QUOTE_LEN: int = 3
    MAX_QUOTE_LEN: int = 100


class Path(BaseSettings):
    RESOURCES: pathlib.Path = "./resources"
    UI_BUILD: str = "../zatrol-ui/build"


class Riot(BaseSettings):
    API_KEY: str = "<key>"


class Settings:
    db = Database()
    const = Const()
    path = Path()
    riot = Riot()
