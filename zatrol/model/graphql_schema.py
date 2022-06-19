import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from zatrol.model.db_schema import Game as GameModel
from zatrol.model.db_schema import Quote as QuoteModel
from zatrol.model.db_schema import Summoner as SummonerModel


class Summoner(SQLAlchemyObjectType):
    class Meta:
        model = SummonerModel
        interfaces = (relay.Node,)


class Quote(SQLAlchemyObjectType):
    class Meta:
        model = QuoteModel
        interfaces = (relay.Node,)


class Game(SQLAlchemyObjectType):
    class Meta:
        model = GameModel
        interfaces = (relay.Node,)


class SummonerData(graphene.Union):
    class Meta:
        types = (Quote, Game)
