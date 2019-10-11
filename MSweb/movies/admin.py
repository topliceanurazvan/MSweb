from django.contrib import admin

from .models import MovieList, MovieListItem, MovieRating

# Register your models here.
admin.site.register(MovieList)
admin.site.register(MovieListItem)
admin.site.register(MovieRating)
