from modeltranslation.translator import register, TranslationOptions
from .models import Category, DirectorActor, Movie, Genre, MovieShoots

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(DirectorActor)
class DirectorActorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'country', 'titlee')

@register(MovieShoots)
class MovieShootsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')