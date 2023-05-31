# Generated by Django 4.1.6 on 2023-05-31 20:34

import articles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0004_remove_blockreferences_id_blockreferences_block"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blockimage",
            name="file_path",
            field=models.FileField(upload_to=articles.models.directory_for_blocks),
        ),
        migrations.AlterField(
            model_name="font",
            name="font_path",
            field=models.FileField(upload_to="fonts/"),
        ),
    ]