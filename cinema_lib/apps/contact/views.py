from django.shortcuts import render, redirect
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Contact
from .forms import ContactForm

class ContactView(View):
    """Подписка по email"""
    def post(self, request):
        email = request.POST.get('email')

        try:
            validate_email(email)
        except ValidationError as e:
            pass
        else:
            Contact.objects.update_or_create(email=email)
        return redirect(request.META.get('HTTP_REFERER'))
