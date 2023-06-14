# Generated by Django 4.1.6 on 2023-06-14 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0009_alter_keywords_keyword"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comments",
            fields=[
                (
                    "block",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="articles.block",
                    ),
                ),
                ("text", models.TextField(max_length=3500)),
            ],
        ),
        migrations.AlterField(
            model_name="answer",
            name="answer",
            field=models.TextField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="blockquiz",
            name="name",
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="questions",
            name="question",
            field=models.TextField(blank=True, max_length=350),
        ),
    ]
