import graphene
import statistics
from statistics import mode
from graphene_django.types import DjangoObjectType
from .models import Genre, Movie, PlayList


class PlayListType(DjangoObjectType):
    class Meta:
        model = PlayList


class GenreType(DjangoObjectType):
    class Meta:
        model = Genre


class MovieType(DjangoObjectType):

    genre = graphene.List(GenreType)

    @graphene.resolve_only_args
    def resolve_genre(self):
        return self.genre.all()

    class Meta:
        model = Movie


class CreatePlayList(graphene.Mutation):

    class Arguments:
        name = graphene.String()
        owner = graphene.Int()
        movie = graphene.List(graphene.ID)

    playList = graphene.Field(PlayListType)

    def mutate(self, info, name, owner=None, movie=None):

        playList = PlayList.objects.create(
            name=name,
            owner_id=owner,
        )

        if movie is not None:
            movie_set = []
            for movie_id in movie:
                movie_object = Movie.objects.get(pk=movie_id)
                movie_set.append(movie_object)
            playList.movie.set(movie_set)

        playList.save()

        return CreatePlayList(
            playList=playList
        )


class UpdatePlayList(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        owner = graphene.Int()
        movie = graphene.List(graphene.ID)

    playList = graphene.Field(PlayListType)

    def mutate(self, info, id, name=None, owner=None, movie=None):
        playList = PlayList.objects.get(pk=id)

        playList.name = name if name is not None else playList.name
        playList.owner = owner if owner is not None else playList.owner

        if movie is not None:
            movie_set = []
            for movie_id in movie:
                movie_object = Movie.objects.get(pk=movie_id)
                movie_set.append(movie_object)
            playList.movie.set(movie_set)

        playList.save()
        return UpdatePlayList(playList=playList)


class AddMovieToPlayList(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        movie = graphene.Int()

    playList = graphene.Field(PlayListType)

    def mutate(self, info, id, name=None, owner=None, movie=None):
        playList = PlayList.objects.get(pk=id)

        if movie is not None:
            movie_object = Movie.objects.get(pk=movie)
            playList.movie.add(movie_object)

        playList.save()
        return AddMovieToPlayList(playList=playList)


class Mutation(graphene.ObjectType):
    create_playList = CreatePlayList.Field()
    update_playlist = UpdatePlayList.Field()
    add_movie_to_playList = AddMovieToPlayList.Field()


class Query(object):

    all_movie = graphene.List(MovieType)

    movie_by_id = graphene.Field(MovieType, id=graphene.Int(required=True))

    create_play_list = graphene.Field(
        PlayListType,
        owner=graphene.Int(required=True),
        name=graphene.String(required=True)
    )

    suggest_movie = graphene.List(MovieType, id=graphene.Int(required=True))

    def resolve_suggest_movie(root, info, **kwargs):
        geners_list = []
        id = kwargs.get('id')
        play = PlayList.objects.get(id=id)

        mov = play.movie.all()
        for m in mov:

            gen = m.genre.all()

            for g in gen:

                geners_list.append(g.id)
        x = max(set(geners_list), key=geners_list.count)

        try:
            return Movie.objects.filter(genre__id=x).exclude(id__in=mov)
        except Movie.DoesNotExist:
            return None

    def resolve_all_movie(root, info):
        # We can easily optimize query count in the resolve method
        return Movie.objects.all()

    def resolve_movie_by_id(root, info, id):
        try:
            return Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return None

    def resolve_create_play_list(root, info, id, name):
        try:
            return PlayList.objects.create(name=name, owner_id=id)
        except PlayList.DoesNotExist:
            return None
