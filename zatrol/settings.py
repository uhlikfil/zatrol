import pathlib

from pydantic.env_settings import BaseSettings


class Database(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "zatrol"
    DB_USER: str = "postgres"
    DB_PASS: str = "root"

    DATABASE_URL: str = None

    @property
    def DB_URI(self):
        DEFAULT_DRIVER = "postgres"
        DRIVER = "postgresql+asyncpg"

        if not self.DATABASE_URL:
            self.DATABASE_URL = f"{DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        elif self.DATABASE_URL.startswith(f"{DEFAULT_DRIVER}://"):
            self.DATABASE_URL = self.DATABASE_URL.replace(DEFAULT_DRIVER, DRIVER, 1)
        return self.DATABASE_URL


class Const(BaseSettings):
    CHAMPS_INTERVAL_H: float = 0.1
    HISTORY_INTERVAL_H: float = 0.1
    MIN_QUOTE_LEN: int = 3
    MAX_QUOTE_LEN: int = 100


class Path(BaseSettings):
    RESOURCES: pathlib.Path = "./resources"
    UI_BUILD: pathlib.Path = "./zatrol-ui/build"


class Riot(BaseSettings):
    API_KEY: str = "<key>"


class Config(BaseSettings):
    SERVE_UI: int = 0


class Settings:
    db = Database()
    const = Const()
    path = Path()
    riot = Riot()
    config = Config()
