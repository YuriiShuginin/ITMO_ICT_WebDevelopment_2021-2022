# Generated by Django 3.2 on 2022-03-27 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yuweather_app', '0003_auto_20220326_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favourite_cities',
            field=models.ManyToManyField(related_name='UserFavourites', through='yuweather_app.Favourite', to='yuweather_app.City', verbose_name='Favourites'),
        ),
    ]