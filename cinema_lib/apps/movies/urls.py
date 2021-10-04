from django.urls import path
from . import views

"""Определяет схемы URL для movies"""

app_name = 'movies'

urlpatterns = [
    path('', views.MoviesView.as_view()),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    #path('<slug:slug>/', views.AddReview.as_view(), name='add_review')
]