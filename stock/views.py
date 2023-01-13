import csv

from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, FormView
from numpy import float64, int64

from statistic.models import Statistic
from stock.forms import DowloadFile, ChoiseTG
from stock.models import Stock, GroupName
import pandas as pd

from utils.parse_site import parse


class DowloadStock(FormView, ListView):
    model = Stock
    context_object_name = 'stock'
    form_class = DowloadFile
    template_name = 'stock/dowl_stock.html'

    def form_valid(self, form):
        """
        Запись в базу с загруженных файлов, удаляет записи по фильтру имени загружаемого склада
        """
        if form.cleaned_data.get('file', False):
            try:
                excel_data_df = pd.read_excel(form.cleaned_data['file'])
                excel_data_df.to_csv('temp.csv')
            except Exception as ex:
                print(ex)
            with open('temp.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['Тип документа'] in ['Отгрузка', 'Подбор', 'Приемка', 'Доставка',
                                                'Внутрискладское перемещение',
                                                'Инвентаризация', 'Самовывоз']:
                        try:
                            type_doc = row['Тип документа']
                            num = 0
                            user = ''
                            if row['Тип документа'] == 'Внутрискладское перемещение':
                                if '->' in row['Название документа']:
                                    type_doc = 'Пст_в_зал'
                                    num = int(
                                        row['Название документа'].split('-')[2].split(',')[0].replace(' ', '').replace(
                                            ',00', ''))
                                else:
                                    type_doc = 'Перенос'
                            try:
                                user = str(row['Исполнитель']).strip()
                            except Exception as ex:
                                print(ex)

                            Statistic.objects.create(
                                id_document=row['ИД документа'],
                                name_document=row['Название документа'],
                                type_document=type_doc,
                                num=num,
                                sklad=row['Склад'],
                                created_at=row['Время создания'],
                                finished_at=row['Время завершения'],
                                status=row['Статус'],
                                user=user,
                            )
                        except Exception as ex:
                            pass
        else:
            for key, value in form.cleaned_data.items():
                if value:
                    excel_data_df = pd.read_excel(value, header=0)
                    try:
                        key_bu = list(excel_data_df.keys()).index('БЮ')
                        key_store = list(excel_data_df.keys()).index('Склад')
                        key_place = list(excel_data_df.keys()).index('Местоположение')
                        key_code = list(excel_data_df.keys()).index('Код \nноменклатуры')
                        key_short_name = list(excel_data_df.keys()).index('Краткое наименование')
                        key_name = list(excel_data_df.keys()).index('Описание товара')
                        key_reason_code = list(excel_data_df.keys()).index('Reason code')
                        key_tg = list(excel_data_df.keys()).index('ТГ')
                        key_ng = list(excel_data_df.keys()).index('НГ')
                        key_physical_num = list(excel_data_df.keys()).index('Физические \nзапасы')
                        key_sale_num = list(excel_data_df.keys()).index('Продано')
                        key_reserve_num = list(excel_data_df.keys()).index('Зарезерви\nровано')
                        key_free_num = list(excel_data_df.keys()).index('Доступно')
                        print(key_bu,
                              key_store,
                              key_place,
                              key_code,
                              key_short_name,
                              key_name,
                              key_reason_code,
                              key_tg,
                              key_ng,
                              key_physical_num,
                              key_sale_num,
                              key_reserve_num,
                              key_free_num, )
                        if form.cleaned_data.get('dowload_full', False):
                            Stock.objects.all().delete()
                        else:
                            Stock.objects.filter(store=excel_data_df.values[0][key_store]).delete()

                        for row in excel_data_df.values:
                            physical_num = 0
                            reserve_num = 0
                            sale_num = 0
                            free_num = 0
                            try:
                                try:
                                    physical_num = int(row[key_physical_num])
                                except Exception as ex:
                                    pass
                                try:
                                    reserve_num = int(row[key_reserve_num])
                                except Exception as ex:
                                    pass
                                try:
                                    sale_num = int(row[key_sale_num])
                                except Exception as ex:
                                    pass
                                try:
                                    free_num = int(row[key_free_num])
                                except Exception as ex:
                                    pass

                                Stock.objects.create(
                                    bu=row[key_bu],
                                    store=row[key_store],
                                    place=row[key_place],
                                    code=row[key_code],
                                    short_name=row[key_short_name],
                                    name=row[key_name],
                                    reason_code=row[key_reason_code],
                                    tg=row[key_tg],
                                    ng=row[key_ng],
                                    physical_num=physical_num,
                                    reserve_num=reserve_num,
                                    sale_num=sale_num,
                                    free_num=free_num)
                            except Exception as ex:
                                print(ex)
                    except ValueError as ex:
                        print('Ненайденно поле', ex)

        return redirect('statistic:statistic')


class StockPage(ListView, FormView):
    model = Stock
    context_object_name = 'stock'
    template_name = 'stock/index.html'
    success_url = 'stock:stock'
    form_class = ChoiseTG

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        main_queryset = self.object_list
        context['groups'] = {}

        groups_list = main_queryset.filter(free_num__gt=0).values_list("tg", flat=True).distinct().order_by(
            'tg')
        for group in groups_list:
            context['groups'][group] = [
                main_queryset.filter(tg=group).values_list("code", flat=True).distinct().count(),
                GroupName.objects.get(tg=group).name
            ]
        return context

    def get_queryset(self):
        queryset_sklad = set(i.code for i in
                             Stock.objects.filter(Q(free_num__gt=0) & Q(store='012_825') | Q(store='011_825')).order_by(
                                 'code'))
        queryset_vls = set(i.code for i in Stock.objects.filter(Q(free_num__gt=0) & Q(store='V_825')).order_by('code'))
        queryset_room = set(
            i.code for i in Stock.objects.filter(Q(free_num__gt=0) & Q(store='A11_825')).order_by('code'))
        queryset_s = set(i.code for i in Stock.objects.filter(Q(free_num__gt=0) & Q(store='S_825')).order_by('code'))

        queryset2 = queryset_sklad.difference(queryset_vls).difference(queryset_room).difference(queryset_s)
        queryset = Stock.objects.filter(free_num__gt=0, code__in=queryset2).order_by('tg')
        return queryset


class GroupPage(ListView):
    model = Stock
    context_object_name = 'stock'
    template_name = 'stock/group_page.html'
    success_url = 'stock:stock_group'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        main_queryset = self.object_list
        code_list = main_queryset.values_list("code", flat=True).distinct().order_by(
            'code')
        context['products'] = {}
        for item in code_list:
            try:
                item_dict = parse(item)
                print(item_dict)
                item_dict['cells'] = [[i.place, i.free_num, i.name] for i in main_queryset.filter(code=item)]
                context['products'][item] = item_dict
            except Exception as ex:
                print(ex)
        return context

    def get_queryset(self):
        queryset_main = Stock.objects.filter(tg=self.kwargs['slug'])

        queryset_sklad = set(i.code for i in
                             queryset_main.filter(Q(free_num__gt=0) & Q(store='012_825') | Q(store='011_825')).order_by(
                                 'code'))
        queryset_vls = set(i.code for i in queryset_main.filter(Q(free_num__gt=0) & Q(store='V_825')).order_by('code'))
        queryset_room = set(
            i.code for i in Stock.objects.filter(Q(free_num__gt=0) & Q(store='A11_825')).order_by('code'))
        queryset_s = set(i.code for i in queryset_main.filter(Q(free_num__gt=0) & Q(store='S_825')).order_by('code'))

        queryset2 = queryset_sklad.difference(queryset_vls).difference(queryset_room).difference(queryset_s)
        queryset = queryset_main.filter(free_num__gt=0, code__in=queryset2).order_by('tg')

        return queryset
