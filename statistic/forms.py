from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets

from django.utils.translation import gettext_lazy as _

from statistic.models import Statistic


class ChoiceBU(forms.Form):
    bu = forms.ChoiceField(label=_('Бизнес юнит'), choices=((i, i) for i in
                                                            sorted(list(set(Statistic.objects.values_list("sklad",
                                                                                                          flat=True).distinct().order_by(
                                                                'sklad'))))),
                           widget=widgets.Select(
                               attrs={'class': 'form-select form-select-lg mb-0'}))
    date_in = forms.DateField(label=_('Начальная дата'),
                              widget=widgets.DateInput(
                                  format='%d-%m-%Y',
                                  attrs={'type': 'date', 'class': 'form-control'}))
    date_finish = forms.DateField(label=_('Конечная дата'),
                                  widget=widgets.DateInput(
                                      format='%d-%m-%Y',
                                      attrs={'type': 'date', 'class': 'form-control'}))
