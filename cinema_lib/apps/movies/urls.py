from django.urls import path
from . import views

"""Определяет схемы URL для movies"""

app_name = 'movies'

urlpatterns = [
    path('', views.MoviesView.as_view(), name='home_page'),
    path('search/', views.Search.as_view(), name='search'),
    path('category_list/', views.CategoryListView.as_view(), name = 'category_list'),
    path('movie_filter/', views.FilterMoviesView.as_view(), name='movie_filter'),
    path('add-rating/', views.AddStarRating.as_view(), name='add_rating'),
    path('json-filter/', views.JsonFilterMoviesView.as_view(), name='json_filter'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    #path('<slug:slug>/', views.AddReview.as_view(), name='add_review'),
    path('add-rating/', views.AddStarRating.as_view(), name='add_rating'),
    path('actor/<str:slug>', views.ActorDetailView.as_view(), name='actor_detail'),
]