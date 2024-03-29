from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth.views import LogoutView

from .views import  (MovieListCreateView, 
                    MovieListDetailView, 
                    HomepageView,
                    UserMovieListView,
                    MovieSearchView,
                    MovieListDeleteView,
                    MovieAddView,
                    MovieRatingView,
                    MovieRatingUpdateView,
                    MovieDeleteView,
                    MovieListUpdateView)

urlpatterns = [
    path('', HomepageView.as_view(), name="home"),
    # path('list/', PublicMovieListView.as_view(), name="public_movie_list"),

    path('mylist/', UserMovieListView.as_view(), name="user_movie_list"),
    path('mylist/create/', MovieListCreateView.as_view(), name="movie_list_create"),
    path('mylist/<slug:slug>/update/', MovieListUpdateView.as_view(), name="movie_list_update"),
    path('mylist/<slug:slug>/', MovieListDetailView.as_view(), name="movie_list_detail"),
    path('mylist/<slug:slug>/search/', MovieSearchView.as_view(), name="movie_search"),
    path('mylist/<slug:slug>/delete/', MovieListDeleteView.as_view(), name="movie_list_delete"),
    path('mylist/<slug:slug>/add/', MovieAddView.as_view(), name="movie_list_add"),
    path('mylist/<slug:slug>/delete_rating/<int:pk>/', MovieDeleteView.as_view(), name="movie_delete"),
    path('mylist/<slug:slug>/rating/<int:pk>/', MovieRatingView.as_view(), name="movie_rating"),
    path('mylist/<slug:slug>/update_rating/<int:pk>/', MovieRatingUpdateView.as_view(), name="movie_update_rating"),
    
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
