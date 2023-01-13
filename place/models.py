from django.db import models


class BU(models.Model):
    name = models.CharField(max_length=10, verbose_name='Бизнес юнит')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Бизнес юнит'
        verbose_name_plural = 'Бизнес юниты'

    def __str__(self):
        return self.name


class Storage(models.Model):
    storage = models.CharField(max_length=20, verbose_name='Склад')
    bu = models.ForeignKey('BU', on_delete=models.CASCADE, verbose_name='БЮ')

    class Meta:
        ordering = ('storage',)
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.storage


class Products(models.Model):
    bu = models.ForeignKey('BU', on_delete=models.CASCADE, verbose_name='БЮ', default='825')
    storage = models.ForeignKey('Storage', on_delete=models.CASCADE, verbose_name='Склад', db_index=True)
    code = models.IntegerField(verbose_name='Код номенклатуры', db_index=True)
    place = models.CharField(max_length=50, verbose_name='Местоположение')
    short_name = models.CharField(max_length=100, verbose_name='Краткое наименование')
    name = models.CharField(max_length=300, verbose_name='Описание товара')
    reason_code = models.CharField(max_length=100, verbose_name='Reason code')
    tn = models.CharField(max_length=100, verbose_name='ТН')
    ng = models.CharField(max_length=100, verbose_name='НГ')
    provider = models.CharField(max_length=300, verbose_name='Поставщик')
    provider_name = models.CharField(max_length=300, verbose_name='Наименование')
    physical_stocks = models.CharField(max_length=5, verbose_name='Физические запасы', blank=True)
    delivery = models.CharField(max_length=5, verbose_name='Передано на доставку', blank=True)
    sales = models.CharField(max_length=5, verbose_name='Продано', blank=True)
    reserved = models.CharField(max_length=5, verbose_name='Зарезервировано', blank=True)
    available = models.CharField(max_length=5, verbose_name='Доступно', blank=True)
    doc_number = models.CharField(max_length=250, verbose_name='Номер документа', blank=True)
    client_number = models.CharField(max_length=250, verbose_name='Счет клиента', blank=True)
    client = models.CharField(max_length=250, verbose_name='Клиент', blank=True)
    week = models.CharField(max_length=50, verbose_name='Неделя', blank=True)
    delivery_type = models.CharField(max_length=5, verbose_name='Тип доставки', blank=True)


    class Meta:
        ordering = ('code',)
        index_together = (('id', 'code', 'storage'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.code
