from django.db import models


class Stock(models.Model):
    bu = models.CharField(verbose_name='БЮ', max_length=10, null=True, blank=True)
    store = models.CharField(verbose_name='Склад', max_length=20, db_index=True)
    place = models.CharField(verbose_name='Местоположение', max_length=20, db_index=True)
    code = models.CharField(verbose_name='Код номенклатуры', max_length=12, db_index=True)
    short_name = models.CharField(verbose_name='Краткое наименование', max_length=50)
    name = models.CharField(verbose_name='Описание товара', max_length=200)
    reason_code = models.CharField(verbose_name='Reason code', max_length=30, default='')
    tg = models.CharField(verbose_name='ТГ', max_length=10)
    ng = models.CharField(verbose_name='НГ', max_length=10)
    physical_num = models.IntegerField(verbose_name='Физические запасы', default=0, db_index=True)
    reserve_num = models.IntegerField(verbose_name='Зарезервировано', default=0)
    sale_num = models.IntegerField(verbose_name='Продано', default=0)
    dost_num = models.IntegerField(verbose_name='Передано на доставку', default=0)
    free_num = models.IntegerField(verbose_name='Доступно', default=0, db_index=True)
    created_at = models.DateTimeField(verbose_name='время записи', auto_created=True, default='2023-01-01 00:00:00')

    class Meta:
        ordering = ('code',)
        index_together = (('store', 'place', 'code', 'physical_num', 'free_num'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class GroupName(models.Model):
    tg = models.CharField(verbose_name='ТГ', max_length=10)
    name = models.CharField(verbose_name='Описание товара', max_length=200)

    class Meta:
        ordering = ('tg',)
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name
