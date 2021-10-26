from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Category, DirectorActor, Genre, Rating
from .forms import ReviewForm, RatingForm

class GenreYear:
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        #print(sorted(Movie.objects.filter(draft=False).values_list("year", flat=True).distinct()))
        return sorted(Movie.objects.filter(draft=False).values_list("year", flat=True).distinct())



class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 3
    paginate_orphans = 1

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

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(','[0])
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


    # def get_context_data(self,**kwargs):
    #     """Получение списка категорий"""
    #     context = super().get_context_data(**kwargs)
    #     context['star_form'] = RatingForm
    #     print(context['star_form'])
    #     return context

    # def get(self, request, slug, **kwargs):
    #     self.object = self.get_object()
    #     context = super().get_context_data(**kwargs)
    #     context['star_form'] = RatingForm(instance=Rating.objects.get(
    #          ip=self.get_client_ip(request),
    #          movie=Movie.objects.get(url=slug).id)
    #          )
    #     print(context['star_form'])
    #     getter = super().get(self, **context)
    #     return getter


    def get(self, request, slug, **kwargs):
        """Вывод оставленного ранее рейтинга"""
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        ip = self.get_client_ip(request)
        movie = Movie.objects.get(url=slug).id
        avg_rating = Rating.objects.filter(movie=movie).aggregate(Avg('star'))['star__avg']
        if avg_rating:
            context['avg_rating'] = avg_rating
        else:
            context['avg_rating'] = 'Будьте первым!'
        if Rating.objects.filter(ip=ip, movie=movie).exists():
            context['star'] = int(str(Rating.objects.get(ip=ip, movie=movie).star))
        else:
            context['star'] = None
        context['form'] = ReviewForm
        context['star_form'] = RatingForm

        return self.render_to_response(context)

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





class JsonFilterMoviesView(ListView):
    """Фильтр фильмов json"""
    def get_queryset(self):
        get_year = self.request.GET.getlist("year")
        get_genres = self.request.GET.getlist("genre")
        if get_year and not get_genres:
            queryset = Movie.objects.filter(year__in=get_year, draft=False).distinct().values(
                "title", "tagline", "url", "poster"
            )
        elif not get_year and get_genres:
            queryset = Movie.objects.filter(genres__in=get_genres, draft=False).distinct().values(
                "title", "tagline", "url", "poster"
            )
        else:
            queryset = Movie.objects.filter(year__in=get_year, genres__in=get_genres, draft=False).distinct().values(
                "title", "tagline", "url", "poster"
            )

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movie_list": queryset}, safe=False)

class AddStarRating(View):
    """Добавление рейтинга к фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(','[0])
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


    def post(self, request):
        form = RatingForm(data=request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
                )
            print(request.POST.get("movie"))
        return redirect('movies:movie_detail', slug=Movie.objects.get(id=request.POST.get("movie")).url)



class CategoryListView(ListView, GenreYear):
    queryset = Category.objects.all()

class FilterMoviesView(GenreYear, ListView):
    """Фильтрация фильмов по году/жанру"""
    paginate_by = 3
    paginate_orphans = 1

    def get_queryset(self):
        get_years = self.request.GET.getlist("year")
        get_genres = self.request.GET.getlist("genre")

        if get_years and not get_genres:
            queryset = Movie.objects.filter(year__in=get_years, draft=False)
        elif not get_years and get_genres:
            queryset = Movie.objects.filter(genres__in=get_genres, draft=False)
        else:
            queryset = Movie.objects.filter(year__in=get_years, genres__in=get_genres, draft=False)

        return queryset

    def get_context_data(self, *args, **kwargs):
        get_years = self.request.GET.getlist("year")
        get_genres = self.request.GET.getlist("genre")

        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f"year={x}&" for x in get_years])
        context['genre'] = ''.join([f"genre={x}&" for x in get_genres])
        return context

class Search(ListView, GenreYear):
    """Поиск по названию"""
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__iregex=self.request.GET.get('q'))

    # Q(title__contains=self.request.GET.get('q').upper()) |
    # Q(title__contains=self.request.GET.get('q').lower()))

    def get_context_data(self, *args, **kwargs):
        search= self.request.GET.get('q')

        context = super().get_context_data(*args, **kwargs)
        context['q'] = f"q={self.request.GET.get('q')}&"
        # print(context['q'])
        # context['search'] = f"search={context['q']}&"
        return context


# class AddReview(View):
#     """Отправка отзывов"""
#     def post(self, request):
#         print(request.POST)
#         return redirect('movies:movie_detail')