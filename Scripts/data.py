import os
import django
import sys
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "explore.settings")
django.setup()

if django:
    from movie.models import Genre, Movie

key = '38a2fbc00dd813dce022db29e3cc91dc'


def insert_genre():
    r = requests.get(
        'https://api.themoviedb.org/3/genre/movie/list?api_key={}'.format(key))
    data = r.json()
    for g in data['genres']:
        Genre.objects.create(name=g['name'], id=g['id'])


# call function
# insert_genre()


def insert_movie():
    r = requests.get(
        'https://api.themoviedb.org/3/movie/top_rated?api_key={}\
&language=en-US&page=11'.format(key))
    data = r.json()
    for m in data['results']:
        print(m['title'])
        movie = Movie.objects.create(
            title=m['title'],
            release_date=m['release_date'],
            overview=m['overview'],
        )
        for i in (m['genre_ids']):
            movie.genre.add(i)


# call function
insert_movie()
