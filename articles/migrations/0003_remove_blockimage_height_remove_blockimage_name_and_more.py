# Generated by Django 4.1.6 on 2023-05-31 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0002_rename_next_block_id_block_next_block_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blockimage",
            name="height",
        ),
        migrations.RemoveField(
            model_name="blockimage",
            name="name",
        ),
        migrations.RemoveField(
            model_name="blockimage",
            name="width",
        ),
    ]