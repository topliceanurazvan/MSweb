from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save

class MovieList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return "User: {0} , List: {1}".format(self.user, self.title)

@receiver(pre_save, sender=MovieList)
def pre_save_movie_list(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.user) + slugify(instance.title)


class MovieListItem(models.Model):
    movie_list = models.ForeignKey(MovieList, on_delete=models.CASCADE, related_name="movies")
    movie_title = models.CharField(max_length=100)

    imdb_id = models.CharField(max_length=50)
    poster = models.URLField()
    plot = models.CharField(max_length=300)

    def __str__(self):
        return "Title: {0}, {1}".format(self.movie_title, self.movie_list)

class MovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="ratings")
    movie = models.ForeignKey(MovieListItem, on_delete=models.CASCADE, blank=True, null=True)

    imdb_id = models.CharField(max_length=50)
    rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        unique_together = ("user", "imdb_id")

    def __str__(self):
        return "User: {0}, imdb_id: {1}".format(self.user, self.imdb_id)