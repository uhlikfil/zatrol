from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from zatrol.model.dbschema import Background, Quote


def insert_quote(session: Session, text: str, champs: list[str]) -> None:
    val = {Quote.text: text, Quote.champ_restrictions: champs}
    update_dict = {Quote.champ_restrictions: champs}
    stmt = insert(Quote).values(val)
    stmt = stmt.on_conflict_do_update(index_elements=[Quote.text], set_=update_dict)
    session.execute(stmt)


def select_random_quote(session: Session) -> Quote:
    stmt = select(Quote).order_by(func.random()).limit(1)
    result = session.execute(stmt).fetchone()
    return result[0] if result else None


def insert_background(session: Session, file_contents: bytes) -> None:
    stmt = insert(Background.img_data).values(file_contents)
    session.execute(stmt)
