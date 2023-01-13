import csv
import os
from pathlib import Path
import io

import pandas as pd
import numpy as np
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, FormView

from cargo.forms import DowloadFileCargo
from stock.models import Stock


class CargoPage(ListView, FormView):
    model = Stock
    context_object_name = 'stock'
    form_class = DowloadFileCargo
    template_name = 'cargo/cargo_page.html'
    object_list = None

    def form_valid(self, form):
        res = []
        for key, value in form.cleaned_data.items():
            if key == 'dowload_cargo':
                try:
                    df = pd.read_excel(value, skiprows=1)

                    df_filter = df[(df["Груз"].notnull()) &
                                   (df["Груз"].str.startswith("P")) |
                                   (df["Груз"].str.startswith("B"))
                                   ]
                    list_r = df_filter["Груз"].tolist()
                except Exception as ex:
                    print(ex)
                    messages.add_message(self.request, messages.WARNING,
                                         'Неверно заполнен файл DVL\nПроблемма: {}'.format(ex))
                    return redirect('cargo:cargo')
            else:
                if value is not None:
                    try:

                        file = value.read().decode('utf-8')
                        reader = csv.reader(io.StringIO(file))
                        reader.__next__()
                        for row in reader:
                            row = row[4].replace('"', '').split(",")
                            res.append(*row)
                    except Exception as ex:
                        print(ex)
                        messages.add_message(self.request, messages.WARNING,
                                             'Неверно заполнен файл сканирования\nПроблемма: {}'.format(ex))
                        return redirect('cargo:cargo')

        list_none = sorted(list(set(list_r).difference(set(res))))
        list_over = sorted(list(set(res).difference(set(list_r))))

        context = self.get_context_data()
        context['none'] = list_none
        context['over'] = list_over
        context['none_dict'] = {}

        for i in list_none:
            try:
                df_new = df[df["Груз"] == i]
                list_new = df_new.values.tolist()[0]
                list_new[0] = int(list_new[0])

                context['none_dict'][i] = list_new
            except Exception as ex:
                print(ex)
                messages.add_message(self.request, messages.WARNING,
                                     'Ошибка сверки\nПроблемма: {}'.format(ex))
                return redirect('cargo:cargo')
        return self.render_to_response(context)
