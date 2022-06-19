import graphene
from flask import Blueprint
from flask_graphql import GraphQLView
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphql.utils import schema_printer

from zatrol.config import Config
from zatrol.database import connection_manager as cm
from zatrol.model import db_schema, graphql_schema


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    summoners = SQLAlchemyConnectionField(graphql_schema.Summoner.connection)
    summoner_data = graphene.List(graphql_schema.SummonerData, puuid=graphene.String())

    @staticmethod
    def resolve_summoner_data(parent, info, **kwargs):
        puuid = kwargs.get("puuid")
        quote_query = graphql_schema.Quote.get_query(info)
        query_data = quote_query.filter(db_schema.Quote.puuid == puuid).all()

        game_query = graphql_schema.Game.get_query(info)
        game_data = game_query.filter(db_schema.Game.puuid == puuid).all()
        return query_data + game_data


schema = graphene.Schema(query=Query)
schema_str = schema_printer.print_schema(schema)
with open(Config.path.resources / "schema.graphql", "w+") as f:
    f.write(schema_str)


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
