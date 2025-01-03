# Generated by Django 4.2 on 2024-10-06 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='email_notifications',
        ),
        migrations.AddField(
            model_name='customuser',
            name='announcement_notifications',
            field=models.BooleanField(default=True, verbose_name='Announcement Notifications'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='news_notifications',
            field=models.BooleanField(default=True, verbose_name='News Notifications'),
        ),
    ]
