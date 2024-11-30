# Generated by Django 4.2 on 2024-10-06 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Category Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('square', models.IntegerField(verbose_name='Square')),
                ('status', models.SmallIntegerField(choices=[(1, 'ACTIVE'), (2, 'SOLD'), (4, 'WITHDRAWN')], verbose_name='Status')),
                ('address', models.CharField(max_length=255, unique=True, verbose_name='Address')),
                ('views', models.IntegerField(default=0, verbose_name='Views')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
            ],
            options={
                'verbose_name': 'Announcement',
                'verbose_name_plural': 'Announcements',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='AnnouncementImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(height_field='image_height', upload_to='announcements/', verbose_name='Image', width_field='image_width')),
                ('image_height', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Image Height')),
                ('image_width', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Image Width')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
            ],
            options={
                'verbose_name': 'Announcement Image',
                'verbose_name_plural': 'Announcement Images',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='AnnouncementViewHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Announcement View History',
                'verbose_name_plural': 'Announcement View Histories',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Category Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000, verbose_name='Comment Text')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('content', models.TextField(max_length=1000, verbose_name='Content')),
                ('views_count', models.IntegerField(default=0, verbose_name='Views Count')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News List',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_in_favorite', models.BooleanField(default=False, verbose_name='Is in Favorite')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='find_house_app.announcement', verbose_name='Announcement')),
            ],
            options={
                'verbose_name': 'Favorite',
                'verbose_name_plural': 'Favorites',
                'ordering': ['-date_added'],
            },
        ),
    ]
