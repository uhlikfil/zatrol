from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from zatrol.config import Config
from zatrol.model.dbschema import metadata

engine: Engine = None
session_mkr: Session = None


def init() -> None:
    global engine
    global session_mkr

    uri = Config.db_connection.database_url.replace("postgres://", "postgresql://")
    engine = create_engine(uri, future=True)
    session_mkr = sessionmaker(engine, autocommit=False)

    metadata.create_all(engine)
