# Generated by Django 4.1.4 on 2023-01-12 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_groupname'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='created_at',
            field=models.DateTimeField(auto_created=True, default='2023-01-06 08:57:35', verbose_name='время записи'),
        ),
    ]