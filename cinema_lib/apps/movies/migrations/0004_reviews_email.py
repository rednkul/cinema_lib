# Generated by Django 3.2.6 on 2021-10-01 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_rename_genre_movie_genres'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]
