# Generated by Django 4.2 on 2024-12-27 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find_house_app', '0010_announcement_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='slug',
            field=models.SlugField(default='', editable=False, max_length=255, unique=True),
        ),
    ]
