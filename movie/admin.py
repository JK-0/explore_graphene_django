from django.contrib import admin
from .models import Genre, Movie, PlayList


# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)
    list_display_links = ('name',)
    search_fields = ('name',)
    list_per_page = 50


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'overview')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_per_page = 100


class PlayListAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)
    list_display_links = ('name',)
    search_fields = ('name',)
    list_per_page = 100


admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(PlayList, PlayListAdmin)
