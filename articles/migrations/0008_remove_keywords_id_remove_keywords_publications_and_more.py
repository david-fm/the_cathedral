# Generated by Django 4.1.6 on 2023-06-10 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0007_alter_blocktitle_title_alter_blocktitle_title_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="keywords",
            name="id",
        ),
        migrations.RemoveField(
            model_name="keywords",
            name="publications",
        ),
        migrations.AddField(
            model_name="keywords",
            name="publications",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to="articles.publication",
            ),
            preserve_default=False,
        ),
    ]