from django import forms

from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Movie, Reviews, Rating, RatingStar



class ReviewForm(forms.ModelForm):
    captcha = ReCaptchaField()
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ('email', 'name', 'text', 'captcha')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border'}) ,
            'text': forms.Textarea(attrs={'class': 'form-control border', "id": "contactcomment"}) ,
        }


class RatingForm(forms.ModelForm):
    """Форма рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ['star',]