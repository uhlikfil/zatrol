from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, BYTEA, ENUM
from sqlalchemy.ext.declarative import declarative_base

from zatrol.model.region import Region

Base = declarative_base()
metadata: MetaData = Base.metadata


class Player(Base):
    __tablename__ = "player"

    puuid = Column(String, primary_key=True)
    region = Column(ENUM(Region))
    summoner_name = Column(String)
    last_match = Column(String)


class Quote(Base):
    __tablename__ = "quote"
    __table_args__ = (UniqueConstraint("puuid", "text"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    puuid = Column("puuid", String, ForeignKey(Player.puuid), index=True)
    text = Column("text", String)
    champ_restrictions = Column(ARRAY(String))


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, autoincrement=True)
    puuid = Column(String, ForeignKey(Player.puuid), index=True)
    img_data = Column(BYTEA)
    champion = Column(String, index=True)


class Background(Base):
    __tablename__ = "background"

    id = Column(Integer, primary_key=True, autoincrement=True)
    img_data = Column(BYTEA)
