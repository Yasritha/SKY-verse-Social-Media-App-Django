# Generated by Django 5.0.7 on 2024-07-19 06:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsdapp', '0005_remove_friendrequest_status_friendrequest_accepted_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='profile_friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
