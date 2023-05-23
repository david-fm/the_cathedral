# Generated by Django 4.1.6 on 2023-05-23 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("articles", "0006_remove_blocktext_font_alter_blocktext_text_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blocktitle",
            name="font",
        ),
        migrations.AlterField(
            model_name="publication",
            name="checks",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="checks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RemoveField(
            model_name="publication",
            name="rates",
        ),
        migrations.AddField(
            model_name="blocktitle",
            name="font",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="articles.font",
            ),
        ),
        migrations.AddField(
            model_name="publication",
            name="rates",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
