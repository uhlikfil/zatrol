# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String
from sqlalchemy.dialects.postgresql import ARRAY, BYTEA
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata: MetaData = Base.metadata


class Quote(Base):
    __tablename__ = "quote"
    text = Column(String, primary_key=True)
    champ_restrictions = Column(ARRAY(String))


class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_data = Column(BYTEA)
    champion = Column(String, index=True)


class Background(Base):
    __tablename__ = "background"
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_data = Column(BYTEA)
