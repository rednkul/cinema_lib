from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget


from .models import Category, Genre, Movie, MovieShoots, DirectorActor, Rating, RatingStar, Reviews
# Register your models here.

admin.site.site_title = "Администрируй тут"
admin.site.site_header = "Администрируй тут"

class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), label="Описание")
    class Meta:
        model = Movie
        labels = {'description': "Описание"}
        fields = '__all__'

def get_fields_names(model):
    """Возвращает названия всех полей модели"""
    return [f"{s}"[f"{s}".rfind('.') + 1:] for s in model._meta.fields]

def get_image(image):
    return mark_safe(f'img src={image} width="5"0 height="auto"')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка страницы категорий"""

    list_display = ("id", "title", "url",)
    list_display_links = ("id", "title", "url",)


class ReviewInLine(admin.TabularInline):
    """Вывод отзывов на страницу фильма"""
    model = Reviews
    readonly_fields = ("name", "email", "text", "parent")
    extra = 0

class MovieShootsInLine(admin.TabularInline):
    model = MovieShoots
    readonly_fields = ('get_image',)
    extra = 0

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="auto">')

    get_image.short_description = ("Изображение")

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Настройка страницы фильмов"""
    list_display = ("id", "title", "url", "draft", "get_poster")
    list_display_links = ("id", "title", "url",)
    list_filter = ("category", "country")
    search_fields = ("title", "category__title", "actors__name", "directors__name")
    inlines = [MovieShootsInLine, ReviewInLine]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    readonly_fields = ("get_poster",)
    form = MovieAdminForm
    actions = ['published', 'unpublished',]
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": (("category", "genres", "country"),)
        }),
        (None, {
            "fields": (("description", "poster", "get_poster"),)
        }),
        ("Actors and directors", {
            "classes": ("collapse",),
            "fields":  (("actors", "directors"), )
        }),
        (None, {
            "fields": (("year", "premiere",),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft",),)
        }),
                )

    def unpublished(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        message_bit = f"Обновлено записей: {row_update}."
        self.message_user(request, f"{message_bit}")

    def published(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        message_bit = f"Обновлено записей: {row_update}."
        self.message_user(request, f"{message_bit}")

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="auto">')

    get_poster.short_description = ("Постер")

    published.short_description = ("Опубликовать")
    published.allowed_permissions = ('change',)

    unpublished.short_description = ("Снять с публикации")
    unpublished.allowed_permissions = ('change',)



@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Настройка страницы отзывов"""
    list_display = ("name", "text", "email", "movie")
    list_display_links = ("name",)
    list_filter = ("name", "movie")
    search_fields = ("name", "text", "movie__title", )
    readonly_fields = ("name", "email", "text", "movie", "parent")
    save_on_top = True


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройка страницы жанров"""
    list_display = ("id", "title", "description")
    list_display_links = ("id", "title")
    search_fields = ("title", "id",)
    save_on_top = True




@admin.register(MovieShoots)
class MovieShootsAdmin(admin.ModelAdmin):
    """Настройка страницы кадров из фильма"""
    list_display = ("id", "title", "get_image")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    fieldsets = (
        (None, {
            "fields": (("title", "movie"),)
                       }),
        (None, {
            "fields": (("description", "get_image"),)
        }),
                )
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="auto">')

    get_image.short_description = ("Изображение")



@admin.register(DirectorActor)
class DirectorActorAdmin(admin.ModelAdmin):
    """Настройка страницы актера/режиссера"""
    list_display = ("name", "id", "get_image")
    list_display_links = ("name", "id")
    search_fields = ("name", "id")

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="auto">')

    get_image.short_description = ("Фото")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Настройка страницы рейтинга"""
    list_display = ("id", "star", "movie", "ip")
    list_display_links = ("id", "ip")
    search_fields = ("ip", "movie")

admin.site.register(RatingStar)
