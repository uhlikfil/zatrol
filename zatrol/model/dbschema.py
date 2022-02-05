# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String
from sqlalchemy.dialects.postgresql import ARRAY, BYTEA
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata: MetaData = Base.metadata


class Champion(Base):
    __tablename__ = "champion"
    name = Column(String, primary_key=True)


class Quote(Base):
    __tablename__ = "quote"
    text = Column(String, primary_key=True)
    champ_restrictions = Column(ARRAY(String))


class Score(Base):
    __tablename__ = "score"
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_data = Column(BYTEA)
    champion = Column(String, ForeignKey(Champion.name), index=True)


class Background(Base):
    __tablename__ = "background"
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_data = Column(BYTEA)
