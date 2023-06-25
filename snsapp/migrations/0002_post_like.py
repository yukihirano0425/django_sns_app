# Generated by Django 4.2.2 on 2023-06-25 02:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='related_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
