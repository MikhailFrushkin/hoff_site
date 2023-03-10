# Generated by Django 4.1.4 on 2023-01-10 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_document', models.CharField(max_length=100, unique=True, verbose_name='документа')),
                ('name_document', models.CharField(max_length=150, verbose_name='Название документа')),
                ('type_document', models.CharField(db_index=True, max_length=50, verbose_name='Тип документа')),
                ('num', models.IntegerField(default=0, verbose_name='Количество')),
                ('sklad', models.CharField(db_index=True, max_length=10, verbose_name='Склад')),
                ('created_at', models.DateTimeField(verbose_name='Время создания')),
                ('finished_at', models.DateTimeField(db_index=True, verbose_name='Время завершения')),
                ('status', models.CharField(max_length=50, verbose_name='Статус')),
                ('user', models.IntegerField(db_index=True, verbose_name='Исполнитель')),
            ],
            options={
                'verbose_name': 'Операция',
                'verbose_name_plural': 'Операции',
                'ordering': ('id_document',),
                'index_together': {('sklad', 'type_document', 'user', 'finished_at')},
            },
        ),
    ]
