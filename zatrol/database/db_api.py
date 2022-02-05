from sqlalchemy import select, tablesample
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from zatrol.model.dbschema import Background, Quote


def insert_quote(session: Session, text: str, champs: list[str]) -> Quote:
    quote = Quote(text, champs)
    session.add(quote)
    return quote


def select_random_quote(session: Session) -> Quote:
    stmt = select(tablesample(Quote, 100)).limit(1)
    return session.execute(stmt).fetchone()


def insert_background(session: Session, file_contents: bytes) -> None:
    stmt = insert(Background.img_data).values(file_contents)
    session.execute(stmt)
