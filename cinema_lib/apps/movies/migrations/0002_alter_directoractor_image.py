# Generated by Django 3.2.6 on 2021-09-29 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directoractor',
            name='image',
            field=models.ImageField(blank=True, upload_to='actors/', verbose_name='Изображение'),
        ),
    ]
