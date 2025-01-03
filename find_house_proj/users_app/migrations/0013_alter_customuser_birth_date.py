# Generated by Django 4.2 on 2024-12-28 09:48

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0012_alter_customuser_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birth_date',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.date(1900, 1, 1)), django.core.validators.MaxValueValidator(datetime.date(2006, 12, 28))], verbose_name='Date of Birth'),
        ),
    ]
