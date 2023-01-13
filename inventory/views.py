import pandas as pd
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, FormView

from inventory.forms import DowloadFileInventory
from inventory.models import Inventory
from utils.parse_site import parse


class InventoryPage(ListView, FormView):
    model = Inventory
    context_object_name = 'inventory'
    form_class = DowloadFileInventory
    template_name = 'inventory/inventory_page.html'
    object_list = None

    def form_valid(self, form):
        Inventory.objects.all().delete()
        context = self.get_context_data()
        context['data'] = {}
        if form.cleaned_data.get('dowload_inventory', False):
            for key, value in form.cleaned_data.items():
                if key == 'dowload_inventory':
                    try:
                        excel_data_df = pd.read_excel(value, skiprows=14)
                        key_store = list(excel_data_df.keys()).index('Склад')
                        key_place = list(excel_data_df.keys()).index('Местоположение')
                        key_code = list(excel_data_df.keys()).index('Код \nноменклатуры')
                        key_short_name = list(excel_data_df.keys()).index('Краткое наименование')
                        key_name = list(excel_data_df.keys()).index('Описание товара')
                        key_reason_code = list(excel_data_df.keys()).index('Reason code')
                        key_tg = list(excel_data_df.keys()).index('ТГ')
                        key_physical_num = list(excel_data_df.keys()).index('Физические \nзапасы')
                        key_sale_num = list(excel_data_df.keys()).index('Продано')
                        key_reserve_num = list(excel_data_df.keys()).index('Зарезерви\nровано')
                        key_free_num = list(excel_data_df.keys()).index('Доступно')
                        key_order = list(excel_data_df.keys()).index('Номер документа')
                        print(
                            key_store,
                            key_place,
                            key_code,
                            key_short_name,
                            key_name,
                            key_reason_code,
                            key_tg,
                            key_physical_num,
                            key_sale_num,
                            key_reserve_num,
                            key_free_num, )

                        for row in excel_data_df.values:
                            if isinstance(row[key_order], float):
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

                                    Inventory.objects.create(
                                        bu='825',
                                        store=row[key_store],
                                        place=row[key_place],
                                        code=row[key_code],
                                        short_name=row[key_short_name],
                                        name=row[key_name],
                                        reason_code=row[key_reason_code],
                                        tg=row[key_tg],
                                        physical_num=physical_num,
                                        reserve_num=reserve_num,
                                        sale_num=sale_num,
                                        free_num=free_num)
                                except Exception as ex:
                                    print(ex)
                    except ValueError as ex:
                        print(ex)
                        messages.add_message(self.request, messages.WARNING,
                                             'Неверно заполнен файл 6.1\nПроблемма: {}'.format(ex))
                        return redirect('inventory:inventory')
                else:
                    if value is not None:
                        try:
                            excel_data_df = pd.read_excel(value)
                            key_code = list(excel_data_df.keys()).index('Код номенклатуры')
                            key_place = list(excel_data_df.keys()).index('Местоположение')
                            key_num = list(excel_data_df.keys()).index('Количество факт')
                            for row in excel_data_df.values:
                                place = row[key_place]
                                code = row[key_code]
                                num = row[key_num]
                                try:
                                    temp = Inventory.objects.get(code=code, place=place)
                                    temp.counted_num = num
                                    temp.save()
                                except Exception as ex:
                                    name = 'Лишний артикул'
                                    try:
                                        product = parse(code)
                                        name = '{}(упаковка из {} шт.)'.format(product['name'], product['box'])
                                    except Exception as ex:
                                        print(ex)

                                    Inventory.objects.create(
                                        bu='825',
                                        store='',
                                        place=place,
                                        code=code,
                                        short_name='',
                                        name=name,
                                        reason_code='',
                                        tg='',
                                        physical_num=0,
                                        reserve_num=0,
                                        sale_num=0,
                                        free_num=0,
                                        counted_num=num
                                    )
                        except Exception as ex:
                            print(ex)
                            messages.add_message(self.request, messages.WARNING,
                                                 'Неверно заполнен файл просчета\nПроблемма: {}'.format(ex))
                            return redirect('inventory:inventory')
            for i in Inventory.objects.all():
                i.delta_num = i.physical_num - i.counted_num
                i.save()
            context['invent'] = Inventory.objects.filter(~Q(delta_num=0))
            return self.render_to_response(context)
        else:
            return redirect('inventory:inventory')
