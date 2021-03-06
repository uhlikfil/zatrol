from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    LargeBinary,
    MetaData,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.ext.declarative import declarative_base

from zatrol.model.region import Region

Base = declarative_base()
metadata: MetaData = Base.metadata


class Summoner(Base):
    __tablename__ = "summoner"

    puuid = Column(String, primary_key=True)
    region = Column(ENUM(Region))
    summoner_name = Column(String)
    last_match = Column(String)


class Quote(Base):
    __tablename__ = "quote"
    __table_args__ = (UniqueConstraint("puuid", "text"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    puuid = Column("puuid", String, ForeignKey(Summoner.puuid, ondelete="cascade"), index=True)  # fmt: skip
    text = Column("text", String)
    champ_restrictions = Column(ARRAY(String))


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, autoincrement=True)
    puuid = Column(String, ForeignKey(Summoner.puuid, ondelete="cascade"), index=True)
    img_data = Column(LargeBinary)
    champion = Column(String, index=True)
