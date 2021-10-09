from django.urls import path
from . import views

"""Определяет схемы URL для movies"""

app_name = 'movies'

urlpatterns = [
    path('', views.MoviesView.as_view()),
    path('movie_filter/', views.FilterMoviesView.as_view(), name='movie_filter'),
    path('json-filter/', views.JsonFilterMoviesView.as_view(), name='json_filter'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    #path('<slug:slug>/', views.AddReview.as_view(), name='add_review'),
    path('actor/<str:slug>', views.ActorDetailView.as_view(), name='actor_detail'),
]