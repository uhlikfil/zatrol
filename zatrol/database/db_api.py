from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection, ResultProxy
from sqlalchemy.sql.expression import func

from zatrol.model.db_schema import Game, Quote, Summoner
from zatrol.model.region import Region


# quotes
def select_quotes(conn: Connection, puuid: str) -> list[Quote]:
    stmt = select(Quote).where(Quote.puuid == puuid)
    return conn.execute(stmt).all()


def select_random_quote(conn: Connection, puuid: str) -> Quote:
    stmt = select(Quote).where(Quote.puuid == puuid)
    stmt = stmt.order_by(func.random()).limit(1)
    return conn.execute(stmt).first()


def insert_quote(conn: Connection, puuid: str, text: str, champs: list[str]) -> None:
    val = {
        Quote.puuid: puuid,
        Quote.text: text,
        Quote.champ_restrictions: champs,
    }
    unique_constr = [Quote.puuid, Quote.text]
    updatable = {Quote.champ_restrictions: champs}
    stmt = insert(Quote).values(val)
    stmt = stmt.on_conflict_do_update(index_elements=unique_constr, set_=updatable)
    conn.execute(stmt)


# summoners
def select_all_summoners(conn: Connection) -> ResultProxy:
    stmt = select(Summoner)
    return conn.execute(stmt)


def select_summoner(conn: Connection, puuid: str) -> Summoner:
    stmt = select(Summoner).where(Summoner.puuid == puuid)
    return conn.execute(stmt).first()


def insert_summoner(
    conn: Connection,
    puuid: str,
    region: Region,
    summoner_name: str,
) -> None:
    value = {
        Summoner.puuid: puuid,
        Summoner.region: region,
        Summoner.summoner_name: summoner_name,
    }
    updatable = {Summoner.region: region, Summoner.summoner_name: summoner_name}
    stmt = insert(Summoner).values(value)
    stmt = stmt.on_conflict_do_update(index_elements=[Summoner.puuid], set_=updatable)
    conn.execute(stmt)


def update_summoner_last_match(conn: Connection, puuid: str, last_match: str) -> None:
    value = {Summoner.last_match: last_match}
    stmt = update(Summoner).where(Summoner.puuid == puuid).values(value)
    conn.execute(stmt)


# games
def insert_game(conn: Connection, puuid: str, img_data: bytes, champion: str) -> None:
    value = {
        Game.puuid: puuid,
        Game.img_data: img_data,
        Game.champion: champion,
    }
    stmt = insert(Game).values(value)
    conn.execute(stmt)


def select_random_game(conn: Connection, puuid: str, champions: list[str]) -> Game:
    stmt = select(Game).where(Game.puuid == puuid)
    if champions:
        stmt = stmt.where(Game.champion.in_(champions))
    stmt = stmt.order_by(func.random()).limit(1)
    return conn.execute(stmt).first()
