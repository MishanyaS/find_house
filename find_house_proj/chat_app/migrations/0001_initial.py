# Generated by Django 4.2 on 2024-10-06 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
            ],
            options={
                'verbose_name': 'Chat',
                'verbose_name_plural': 'Chats',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000, verbose_name='Content')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is Deleted')),
                ('is_edited', models.BooleanField(default=False, verbose_name='Is Edited')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat_app.chat', verbose_name='Chat')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Message',
                'ordering': ['timestamp'],
            },
        ),
    ]
