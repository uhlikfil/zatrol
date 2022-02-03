from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from zatrol.config import Config

engine: Engine = None
session_mkr: Session = None


def init():
    global engine
    global session_mkr

    host = Config.db_connection.host
    username = Config.db_connection.username
    password = Config.db_connection.password
    database = Config.db_connection.database
    connection_str = f"postgresql://{username}:{password}@{host}/{database}"

    engine = create_engine(connection_str, future=True)
    session_mkr = sessionmaker(engine, autocommit=False)

    metadata.create_all(engine)
