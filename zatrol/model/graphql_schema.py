import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.types import ORMField

from zatrol.model.db_schema import Game as GameModel
from zatrol.model.db_schema import Quote as QuoteModel
from zatrol.model.db_schema import Summoner as SummonerModel
from zatrol.model.region import Region

GQLRegion = graphene.Enum.from_enum(Region)


class Summoner(SQLAlchemyObjectType):
    class Meta:
        model = SummonerModel
        interfaces = (relay.Node,)
        exclude_fields = ("last_match",)

    region = ORMField(type=GQLRegion)


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


class MutationResult(graphene.ObjectType):
    ok = graphene.Boolean()
    error = graphene.String(required=False)
