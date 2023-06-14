# Generated by Django 4.1.6 on 2023-06-10 10:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("articles", "0004_remove_blockreferences_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blockreferences",
            name="authors",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]