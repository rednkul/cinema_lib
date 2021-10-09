from django import forms
from .models import Movie, Reviews, Rating, RatingStar

class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ('email', 'name', 'text')


class RatingForm(forms.ModelForm):
    """Форма рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ['star',]