from django.shortcuts import render
from django.views.generic import CreateView


from .models import Contact
from .forms import ContactForm

class ContactView(CreateView):
    """Подписка по email"""
    model = Contact
    form_class = ContactForm
    success_url = '/'



