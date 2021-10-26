# Generated by Django 3.2.6 on 2021-10-03 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_remove_reviews_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directoractor',
            name='image',
            field=models.ImageField(blank=True, upload_to='actors/', verbose_name='Файл фотографии'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(upload_to='movies/', verbose_name='Файл постера'),
        ),
        migrations.AlterField(
            model_name='movieshoots',
            name='image',
            field=models.ImageField(upload_to='movie_shots/', verbose_name='Файл кадра'),
        ),
    ]