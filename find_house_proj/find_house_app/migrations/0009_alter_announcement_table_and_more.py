# Generated by Django 4.2 on 2024-12-24 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('find_house_app', '0008_delete_newscomment'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='announcement',
            table='announcement',
        ),
        migrations.AlterModelTable(
            name='announcementimage',
            table='announcement_image',
        ),
        migrations.AlterModelTable(
            name='announcementviewhistory',
            table='announcement_view_history',
        ),
        migrations.AlterModelTable(
            name='category',
            table='category',
        ),
        migrations.AlterModelTable(
            name='comment',
            table='comment',
        ),
        migrations.AlterModelTable(
            name='favorite',
            table='favorite',
        ),
        migrations.AlterModelTable(
            name='news',
            table='news',
        ),
    ]
