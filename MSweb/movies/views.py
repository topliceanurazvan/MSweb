import omdb

API_KEY = '202005fe'
omdb.set_default('apikey', API_KEY)

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView, RedirectView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from itertools import chain

from .models import MovieList, MovieListItem, MovieRating

class HomepageView(TemplateView):
    template_name = "movies/homepage.html"

class PublicMovieListView(ListView):
    template_name = "movies/movie_list.html"
    model = MovieList

class UserMovieListView(ListView):
    template_name = "movies/user_movie_list.html"
    model = MovieList

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user) # show only current users list 

class MovieListCreateView(CreateView):
    template_name = "movies/create_movie_list.html"
    model = MovieList
    fields = ['title', 'description']

    def get_success_url(self, **kwargs):
        return reverse_lazy('movie_list_detail', args = (self.object.slug,))

    def form_valid(self, form):
        movie_list = form.save(commit=False)
        movie_list.user = self.request.user
        movie_list.save()
        return super(MovieListCreateView, self).form_valid(form)

class MovieListDetailView(ListView):
    template_name = "movies/movie_list_detail.html"
    model = MovieListItem

    def get_queryset(self, *args, **kwargs):
        return MovieList.objects.get(slug = self.kwargs['slug']).movies.all() #show only current list movies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movielist'] = MovieList.objects.get(slug=self.kwargs['slug']) # used for showing the list title in the listview
    
        movie_list = context['object_list']
        for movie in movie_list:
            try:
                object_rating = MovieRating.objects.get(imdb_id=movie.imdb_id)
                movie.rating = object_rating.rating
            except MovieRating.DoesNotExist:
                object_rating = None

        return context

class MovieSearchView(TemplateView):
    template_name = "movies/movie_search.html"
    model = MovieList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('movie_title')
        context['slug'] = self.kwargs['slug']
        context['title'] = title
        context['omdb'] = omdb.search(title)
        return context


class MovieListDeleteView(DeleteView):
    template_name = "movies/movie_list_delete.html"
    model = MovieList

    def get_success_url(self, **kwargs):
         return reverse_lazy('user_movie_list')

    def get_object(self):
        print (self.kwargs['slug'])
        return get_object_or_404(MovieList, slug=self.kwargs['slug'])
    
    def delete(self, request, *args, **kwargs):
        return super(MovieListDeleteView, self).delete(request, *args, **kwargs)

class MovieAddView(RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):

        imdbID = self.request.GET.get('imdb_id')
        omdbItem = dict()
        omdbItem = omdb.imdbid(imdbID)
        movie_list = MovieList.objects.get(slug=self.kwargs['slug'])

        item = MovieListItem(movie_list=movie_list, movie_title=omdbItem['title'], imdb_id=imdbID, poster=omdbItem['poster'], plot=omdbItem['plot'])
        item.save();

        return reverse_lazy('movie_list_detail', kwargs = {'slug': self.kwargs['slug']})

class MovieRatingView(CreateView):
    template_name = "movies/movie_rating_create_update.html"
    model = MovieRating
    fields=['rating']

    def get_success_url(self, **kwargs):
        return reverse_lazy('movie_list_detail', kwargs = {'slug': self.kwargs['slug']})

    def form_valid(self, form):
        movie_rating = form.save(commit=False)
        movie_rating.user = self.request.user
        movie_rating.movie = get_object_or_404(MovieListItem, slug=self.kwargs['slug_item'])
        movie_rating.imdb_id = self.request.GET.get('imdb_id')
        movie_rating.save()
        return super(MovieRatingView, self).form_valid(form)
        
class MovieRatingUpdateView(UpdateView):
    template_name = "movies/movie_rating_create_update.html"
    model = MovieRating
    fields=['rating']

    def get_success_url(self, **kwargs):
        return reverse_lazy('movie_list_detail', kwargs = {'slug': self.kwargs['slug']})

    def get_object(self):
        imdbID = self.request.GET.get('imdb_id')
        return get_object_or_404(MovieRating, imdb_id = imdbID)


class MovieDeleteView(DeleteView):
    template_name = "movies/movie_delete.html"
    model = MovieListItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']

        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('movie_list_detail', kwargs = {'slug': self.kwargs['slug']})
        
    def get_object(self):
        return get_object_or_404(MovieListItem, slug=self.kwargs['slug_item'])

    def delete(self, request, *args, **kwargs):
        return super(MovieDeleteView, self).delete(request, *args, **kwargs)

def logout(request):
    logout(request)
