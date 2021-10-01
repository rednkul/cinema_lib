from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie

class MoviesView(ListView):
    """Список фильмов"""
    #def get(self, request):
    queryset = Movie.objects.filter(draft=False)
    context = {"movie_list": queryset}
        #return render(request, template_name, context)

class MovieDetailView(DetailView):
    """Информация о фильме"""
    model = Movie
    slug_field = "url"