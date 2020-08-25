from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    overview = models.CharField(max_length=9000)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class PlayList(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name
