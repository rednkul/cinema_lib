from django.db import models

class Contact(models.Model):
    """Подписка по email"""
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Email-адрес'
        verbose_name_plural = 'Email-адреса'


    def __str__(self):
        return self.email