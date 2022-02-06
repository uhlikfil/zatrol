from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from zatrol.model.dbschema import Background, Player, Quote
from zatrol.model.region import Region


# quotes
def insert_quote(
    session: Session, player_puuid: str, text: str, champs: list[str]
) -> None:
    val = {
        Quote.player_puuid: player_puuid,
        Quote.text: text,
        Quote.champ_restrictions: champs,
    }
    unique_constr = [Quote.player_puuid, Quote.text]
    updatable = {Quote.champ_restrictions: champs}
    stmt = insert(Quote).values(val)
    stmt = stmt.on_conflict_do_update(index_elements=unique_constr, set_=updatable)
    session.execute(stmt)


def select_random_quote(session: Session, player_puuid: str) -> Quote:
    stmt = select(Quote).where(Player.puuid == player_puuid)
    stmt = stmt.order_by(func.random()).limit(1)
    result = session.execute(stmt).scalar()
    return result


# backgrounds
def insert_background(session: Session, file_contents: bytes) -> None:
    stmt = insert(Background.img_data).values(file_contents)
    session.execute(stmt)


# players
def select_all_players(session: Session) -> list[Player]:
    stmt = select(Player)
    return list(session.execute(stmt).scalars())


def insert_player(
    session: Session,
    puuid: str,
    region: Region,
    summoner_name: str,
    last_start_time: int,
) -> None:
    value = {
        Player.puuid: puuid,
        Player.region: region,
        Player.summoner_name: summoner_name,
        Player.last_match_start_time: last_start_time,
    }
    updatable = {Player.region: region, Player.summoner_name: summoner_name}
    stmt = insert(Player).values(value)
    stmt = stmt.on_conflict_do_update(index_elements=[Player.puuid], set_=updatable)
    session.execute(stmt)
