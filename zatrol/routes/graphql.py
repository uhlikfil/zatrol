import graphene
from flask import Blueprint
from flask_graphql import GraphQLView
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphql.utils import schema_printer

from zatrol.config import Config
from zatrol.database import connection_manager as cm
from zatrol.exception import error_handlers
from zatrol.model import db_schema, graphql_schema
from zatrol.model.region import Region
from zatrol.services import quote as quote_svc
from zatrol.services import summoner as summoner_svc


class RegisterSummoner(graphene.Mutation):
    class Arguments:
        region = graphql_schema.GQLRegion()
        summoner_name = graphene.String()

    result = graphene.Field(lambda: graphql_schema.MutationResult)

    @error_handlers.mutate_wrapper
    def mutate(self, info, region, summoner_name):
        summoner_svc.insert_summoner(Region(region), summoner_name)


class RegisterQuote(graphene.Mutation):
    class Arguments:
        puuid = graphene.String()
        text = graphene.String()
        champ_restrictions = graphene.List(graphene.String, required=False)

    result = graphene.Field(lambda: graphql_schema.MutationResult)

    @error_handlers.mutate_wrapper
    def mutate(self, info, puuid, text, champ_restrictions=[]):
        quote_svc.add_quote(puuid, text, champ_restrictions)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    summoners = SQLAlchemyConnectionField(graphql_schema.Summoner.connection)
    summoner_data = graphene.List(graphql_schema.SummonerData, puuid=graphene.String())

    @staticmethod
    def resolve_summoner_data(parent, info, puuid):
        quote_query = graphql_schema.Quote.get_query(info)
        query_data = quote_query.filter(db_schema.Quote.puuid == puuid).all()

        game_query = graphql_schema.Game.get_query(info)
        game_data = game_query.filter(db_schema.Game.puuid == puuid).all()
        return query_data + game_data


class Mutations(graphene.ObjectType):
    register_summoner = RegisterSummoner.Field()
    register_quote = RegisterQuote.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)

blueprint = Blueprint("graphql", __name__, url_prefix="/api")

blueprint.add_url_rule(
    "graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
        get_context=lambda: {"session": cm.db_session},
    ),
)


# Dump schema
schema_str = schema_printer.print_schema(schema)
with open(Config.path.resources / "schema.graphql", "w+") as f:
    f.write(schema_str)
