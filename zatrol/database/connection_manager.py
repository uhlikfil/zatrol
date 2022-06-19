from sa_decor import set_global_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from zatrol.config import Config
from zatrol.model.db_schema import metadata

db_session = None


def init() -> None:
    global db_session
    uri = Config.db_connection.database_url.replace("postgres://", "postgresql://")
    engine = create_engine(uri, future=True)
    set_global_engine(engine)
    db_session = scoped_session(
        sessionmaker(bind=engine, autocommit=False, autoflush=False)
    )

    # TODO Alembic?
    metadata.create_all(engine)
