from django.contrib import admin
from .models import Category, Genre, Movie, MovieShoots, DirectorActor, Rating, RatingStar, Reviews
# Register your models here.

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieShoots)
admin.site.register(DirectorActor)
admin.site.register(Rating)
admin.site.register(RatingStar)
admin.site.register(Reviews)