from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie
from .forms import ReviewForm

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








class AddReview(View):
    """Отправка отзывов"""
    def post(self, request):
        print(request.POST)
        return redirect('movies:movie_detail')