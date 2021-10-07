from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Category, DirectorActor, Genre
from .forms import ReviewForm

class GenreYear:
    """Жаны и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values_list("year", flat=True).distinct()


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    queryset = Movie.objects.filter(draft=False)
    #context = {"movie_list": queryset}

    # def get_context_data(self, *args, **kwargs):
    #     """Получение списка категорий"""
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context


class MovieDetailView(GenreYear, DetailView):
    """Информация о фильме"""
    model = Movie
    slug_field = "url"

    # def get_context_data(self, *args, **kwargs):
    #     """Получение списка категорий"""
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context

    def post(self, request, slug):
        """Отправка формы отзыва"""
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie_id = Movie.objects.get(url=slug).id
            form.save()
        return redirect('movies:movie_detail', slug=slug)

class ActorDetailView(GenreYear, DetailView):
    """Страница актера/режиссера"""
    model = DirectorActor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    """Фильтрация фильмов по году/жанру"""

    def get_queryset(self):
        get_year = self.request.GET.getlist("year")
        get_genres = self.request.GET.getlist("genre")

        if get_year and not get_genres:
            queryset = Movie.objects.filter(year__in=get_year, draft=False)
        elif not get_year and get_genres:
            queryset = Movie.objects.filter(genres__in=get_genres, draft=False)
        else:
            queryset = Movie.objects.filter(year__in=get_year, genres__in=get_genres, draft=False)

        return queryset



# class AddReview(View):
#     """Отправка отзывов"""
#     def post(self, request):
#         print(request.POST)
#         return redirect('movies:movie_detail')