# Generated by Django 4.1.4 on 2023-10-12 08:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweeetr', '0004_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweeet',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='tweeet', to=settings.AUTH_USER_MODEL),
        ),
    ]
