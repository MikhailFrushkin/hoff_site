import csv
from datetime import datetime, date, time, timedelta

import pandas as pd
from django.contrib import messages
from django.db.models import Count, Sum, F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView, FormView

from place.forms import UploadFile
from statistic.forms import ChoiceBU
from statistic.models import Statistic


class StatisticMainPage(ListView, FormView):
    model = Statistic
    context_object_name = 'statistic'
    form_class = ChoiceBU
    template_name = 'statistic/index.html'
    success_url = 'statistic:statistic'
    object_list = None
    initial = {'bu': '825'}
    queryset = Statistic.objects.filter(sklad='825').filter(finished_at__year='2023', finished_at__month='1')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        main_queryset = self.object_list

        context['pickup'] = main_queryset.filter(type_document='Подбор', name_document__icontains='Самовывоз').order_by(
            'finished_at')

        date_list = sorted(list(
            set([i.date() for i in main_queryset.values_list("finished_at", flat=True).distinct()])))
        context['date_list'] = date_list
        try:
            context['date_first'] = date_list[0]
            context['date_last'] = date_list[-1]
        except Exception as ex:
            print(ex)
            messages.add_message(self.request, messages.WARNING,
                                 'Нет данных за период')

        operations = ['Отгрузка', 'Подбор', 'Приемка', 'Доставка', 'Перенос', 'Пст_в_зал', 'Инвентаризация',
                      'Самовывоз']
        all_operations_count = main_queryset.count()
        context['all'] = {}
        context['all_operation_day'] = []
        context['all_operations_count'] = all_operations_count
        for item in operations:
            num_item = main_queryset.filter(type_document=item).count()
            if all_operations_count:
                num_proc = num_item / all_operations_count * 100
            else:
                num_proc = 0
            context['all'][item] = [num_item, round(num_proc, 1)]

            context[item] = []
            for i in date_list:
                num_oper = main_queryset.filter(finished_at__date=i, type_document=item).values(
                    'type_document').count()
                context[item].append(num_oper)

        context['sorted_all'] = sorted(context['all'].items(), key=lambda x: x[1][1], reverse=True)

        for i in date_list:
            num_day = main_queryset.filter(finished_at__date=i).values('type_document').count()
            context['all_operation_day'].append(num_day)

        summa_pst = main_queryset.filter(type_document='Пст_в_зал').aggregate(Sum('num'))
        context['summa_pst'] = summa_pst['num__sum']
        user_list = sorted(list(set(main_queryset.values_list("user", flat=True).distinct().order_by('user'))))
        context['users'] = {}
        for user in user_list:
            context['users'][user] = {'all': [0, 0]}
            for item in operations:
                user_operations = main_queryset.filter(user=user, type_document=item).count()
                context['users'][user][item] = user_operations
                context['users'][user]['all'][0] += user_operations
                context['users'][user]['all'][1] = main_queryset.filter(user=user).aggregate(Sum('num'))['num__sum']

        return context

    def form_valid(self, form):
        cd = form.cleaned_data
        if cd['date_in'] > cd['date_finish']:
            messages.add_message(self.request, messages.WARNING,
                                 'Конечная дата должна быть больше начальной!')
            return redirect(self.success_url)

        main_queryset = Statistic.objects.filter(sklad=cd['bu']).filter(
            finished_at__range=(cd['date_in'], cd['date_finish'] + timedelta(days=1)))

        self.object_list = main_queryset
        context = self.get_context_data()

        return self.render_to_response(context)
