from django.db import models


class Statistic(models.Model):
    id_document = models.CharField(unique=True, max_length=100, verbose_name='документа')
    name_document = models.CharField(max_length=150, verbose_name='Название документа')
    type_document = models.CharField(max_length=50, verbose_name='Тип документа', db_index=True)
    num = models.IntegerField(verbose_name='Количество', default=0)
    sklad = models.CharField(max_length=10, verbose_name='Склад', db_index=True)
    created_at = models.DateTimeField(verbose_name='Время создания')
    finished_at = models.DateTimeField(verbose_name='Время завершения', db_index=True)
    status = models.CharField(max_length=50, verbose_name='Статус')
    user = models.IntegerField(verbose_name='Исполнитель', db_index=True)

    class Meta:
        ordering = ('id_document',)
        index_together = (('sklad', 'type_document', 'user', 'finished_at'),)
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    def __str__(self):
        return self.name_document
