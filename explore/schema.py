import movie.schema
import graphene

from graphene_django.debug import DjangoDebug


class Query(
    movie.schema.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(movie.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
