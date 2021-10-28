from django.db import models
from django.urls import reverse

from datetime import date


from django.utils.translation import gettext_lazy as _




class Category(models.Model):
    """Категории"""
    title = models.CharField("Категория", max_length=30)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160)
    image = models.ImageField("Файл постера", upload_to="categories/", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        # verbose_name_en = "Category"
        # verbose_name_plural_en = "Categories"




class DirectorActor(models.Model):
    """Режиссеры и актеры"""
    name = models.CharField("Имя", max_length=30)
    age = models.SmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Файл фотографии", upload_to="actors/", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    """Жанры"""
    title = models.CharField(max_length=40)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """Фильмы"""
    title = models.CharField("Фильм",max_length=50)
    tagline = models.CharField("Слоган",max_length=60, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Файл постера", upload_to='movies/')
    year = models.PositiveSmallIntegerField("Год выхода", default=2021)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(DirectorActor, verbose_name="Режиссер", related_name="film_director")
    actors = models.ManyToManyField(DirectorActor, verbose_name="Актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    premiere = models.CharField("Премьера", max_length=30, default=date.today)
    budget = models.PositiveIntegerField("Бюджет", help_text="Сумма в $")
    fees_in_usa = models.PositiveIntegerField("Сборы в США", default=0, help_text="Сумма в $")
    fees_in_world = models.PositiveIntegerField("Сборы в мире", default=0, help_text="Сумма в $")
    category = models.ForeignKey(Category, verbose_name="Категории", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Черновик", default=False)
    titlee = models.CharField(
        max_length=500,
        verbose_name=_("TITLE"),
        help_text=_("HELP_TITLE"),
        default=''
    )


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        #ordering = ['-id']


class MovieShoots(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание", max_length=100)
    image = models.ImageField("Файл кадра", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ['-value']



class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=25)
    star = models.ForeignKey(RatingStar, verbose_name="Звезда рейтинга", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"






class Reviews(models.Model):
    email = models.EmailField(default='')
    name = models.CharField("Имя автора", max_length=50)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
            'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
                               )
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

