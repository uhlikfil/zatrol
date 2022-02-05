from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from zatrol.model.dbschema import Champion


def insert_champions(session: Session, champ_names: list[str]) -> None:
    stmt = insert(Champion).values([{Champion.name: name} for name in champ_names])
    stmt = stmt.on_conflict_do_nothing(index_elements=[Champion.name])
    session.execute(stmt)
