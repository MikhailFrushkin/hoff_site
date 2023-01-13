import csv
import pandas as pd

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView

from place.forms import UploadFile
from place.models import Products, BU, Storage


class DowloadFile(FormView):
    form_class = UploadFile
    template_name = 'place/dowload_file.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            return context
        raise Http404

    def form_valid(self, form):
        try:
            excel_data_df = pd.read_excel(form.cleaned_data['file'], skiprows=13, header=1)
            excel_data_df.to_csv('temp.csv')
        except Exception as ex:
            print(ex)
        bu = BU.objects.get(name='825')
        with open('temp.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    temp = Products.objects.create(
                        bu=bu,
                        storage=Storage.objects.get(storage=row['Склад']),
                        code=row['Код \nноменклатуры'],
                        place=row['Местоположение'],
                        short_name=row['Краткое наименование'],
                        name=row['Описание товара'],
                        reason_code=row['Reason code'],
                        tn=row['ТГ'],
                        ng=row['НГ'],
                        provider=row['Поставщик'],
                        provider_name=row['Наименование'],
                        physical_stocks=row['Физические \nзапасы'],
                        delivery=row['Передано на доставку'],
                        sales=row['Продано'],
                        reserved=row['Зарезерви\nровано'],
                        available=row['Доступно'],
                        doc_number=row['Номер документа'],
                        client_number=row['Счет клиента'],
                        client=row['Клиент'],
                        week=row['Неделя'],
                        delivery_type=row['Способ \nдоставки'],
                    )
                except Exception as ex:
                    print(ex)

        return redirect('main:main_page')
