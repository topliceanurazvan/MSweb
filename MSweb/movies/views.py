import omdb

API_KEY = '202005fe'
omdb.set_default('apikey', API_KEY)

from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView, RedirectView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from itertools import chain
from django.db.models import Count, Avg
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.exceptions import ValidationError

from .models import MovieList, MovieListItem, MovieRating

class HomepageView(TemplateView):
    template_name = "movies/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = MovieRating.objects.values('imdb_id').annotate(avg_rating=Avg('rating')).order_by('-avg_rating')
        top_movies = []
        for item in results[:3]:
            movie = MovieListItem.objects.filter(imdb_id = item["imdb_id"]).first()
            movie.rating = item['avg_rating']
            top_movies.append(movie)
        context['top_movies'] = top_movies
        return context
   
class PublicMovieListView(ListView):
    template_name = "movies/movie_list.html"
    model = MovieList

class UserMovieListView(LoginRequiredMixin, ListView):
    template_name = "movies/user_movie_list.html"
    model = MovieList

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user) # show only current users list 

class MovieListCreateView(LoginRequiredMixin, CreateView):
    template_name = "movies/movie_list_create.html"
    model = MovieList
    fields = ['title', 'description']

    def get_success_url(self, **kwargs):
        return reverse_lazy('movie_list_detail', args = (self.object.slug,))

    def form_valid(self, form):
        movie_list = form.save(commit=False)
        movie_list.user = self.request.user
        title = form.cleaned_data.get('title')
        for m in MovieList.objects.all():
            if title == m.title:
                form.add_error('title', ValidationError("List name already exists!"))
                return super().form_invalid(form)
        return super().form_valid(form)

class MovieListUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "movies/movie_list_create.html"
    model = MovieList
    fields = ['title', 'description']

    def get_success_url(self, **kwargs):
        return reverse_lazy('user_movie_list')
    
    def form_valid(self, form):
        movie_list = form.save(commit=False)
        title = form.cleaned_data.get('title')
        for m in MovieList.objects.all():
            if title == m.title:
                form.add_error('title', ValidationError("List name already exists!"))
                return super().form_invalid(form)
        return super().form_valid(form)

class MovieListDetailView(LoginRequiredMixin, ListView):
    template_name = "movies/movie_list_detail.html"
    model = MovieListItem

    def get_queryset(self, *args, **kwargs):
        queryset = MovieList.objects.get(slug = self.kwargs['slug']).movies.all()#show only current list movies
        
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movielist'] = MovieList.objects.get(slug=self.kwargs['slug']) # used for showing the list title in the listview
    
        movie_list = context['object_list']
        for movie in movie_list:
            try:
                object_rating = MovieRating.objects.get(imdb_id=movie.imdb_id, user=self.request.user)
                movie.rating = object_rating.rating
            except MovieRating.DoesNotExist:
                object_rating = None

        return context

class MovieSearchView(LoginRequiredMixin, TemplateView):
    template_name = "movies/movie_search.html"
    model = MovieList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get('movie_title')
        context['slug'] = self.kwargs['slug']
        context['title'] = title

        omdb_result = omdb.search(title)

        for item in omdb_result:
            item['exists'] = MovieListItem.objects.filter(
                movie_list__user=self.request.user,
                imdb_id=item['imdb_id'],
                movie_list__slug=self.kwargs['slug']
            ).exists()

        context['omdb'] = omdb_result

        return context

class MovieListDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "movies/movie_list_delete.html"
    model = MovieList

    def get_success_url(self, **kwargs):
         return reverse_lazy('user_movie_list')

    def get_object(self):
        print (self.kwargs['slug'])
        return get_object_or_404(MovieList, slug=self.kwargs['slug'])
    
    def delete(self, request, *args, **kwargs):
        return super(MovieListDeleteView, self).delete(request, *args, **kwargs)

class MovieAddView(LoginRequiredMixin, RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):

        imdbID = self.request.GET.get('imdb_id')
        omdbItem = dict()
        omdbItem = omdb.imdbid(imdbID)
        movie_list = MovieList.objects.get(slug=self.kwargs['slug'])
        
        item = MovieListItem(movie_list=movie_list, movie_title=omdbItem['title'], imdb_id=imdbID, poster=omdbItem['poster'], plot=omdbItem['plot'])
        item.save();

        return reverse_lazy('movie_list_detail', kwargs = {'slug': self.kwargs['slug']})

class MovieRatingView(LoginRequiredMixin, CreateView):
    template_name = "movies/movie_rating_create_update.html"
    model = MovieRating
    fields=['rating']

    def get_success_url(self, **kwargs):
        return reverse_lazy('movie_list_detail', kwargs = {'slug': self.kwargs['slug']})

    def form_valid(self, form):
        movie_rating = form.save(commit=False)
        movie_rating.user = self.request.user
        movie_rating.movie = get_object_or_404(MovieListItem, pk=self.kwargs['pk'])
        movie_rating.imdb_id = self.request.GET.get('imdb_id')
        movie_rating.save()
        return super(MovieRatingView, self).form_valid(form)
        
class MovieRatingUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "movies/movie_rating_create_update.html"
    model = MovieRating
    fields=['rating']

    def get_success_url(self, **kwargs):
        return reverse_lazy('movie_list_detail', kwargs = {'slug': self.kwargs['slug']})

    def get_object(self):
        imdbID = self.request.GET.get('imdb_id')
        return get_object_or_404(MovieRating, imdb_id = imdbID)

class MovieDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "movies/movie_delete.html"
    model = MovieListItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']

        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('movie_list_detail', kwargs = {'slug': self.kwargs['slug']})
        
    def get_object(self):
        return get_object_or_404(MovieListItem, pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        return super(MovieDeleteView, self).delete(request, *args, **kwargs)

def logout(request):
    logout(request)
