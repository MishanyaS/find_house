# Generated by Django 4.2 on 2024-10-28 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('find_house_app', '0006_alter_announcement_description_alter_news_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000, verbose_name='Comment Text')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newscomments', to='find_house_app.news', verbose_name='News')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'News Comment',
                'verbose_name_plural': 'News Comments',
                'ordering': ['-date_added'],
            },
        ),
    ]
