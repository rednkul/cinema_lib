from django import forms
from .models import Movie, Reviews

class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ('email', 'name', 'text')