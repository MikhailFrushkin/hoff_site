from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets

from django.utils.translation import gettext_lazy as _

from statistic.models import Statistic
from stock.models import Stock

choice_groups = Stock.objects.filter(free_num__gt=0).values_list("tg", flat=True).distinct().order_by('tg')


class DowloadFile(forms.Form):
    dowload_011 = forms.FileField(label=_('011 склад'), required=False,
                                  widget=forms.ClearableFileInput(attrs={'class': 'btn btn-sm btn-outline-secondary'}))
    dowload_012 = forms.FileField(label=_('012 склад'), required=False,
                                  widget=forms.ClearableFileInput(attrs={'class': 'btn btn-sm btn-outline-secondary'}))
    dowload_vls = forms.FileField(label=_('vsl склад'), required=False,
                                  widget=forms.ClearableFileInput(attrs={'class': 'btn btn-sm btn-outline-secondary'}))
    dowload_a11 = forms.FileField(label=_('room склад'), required=False,
                                  widget=forms.ClearableFileInput(attrs={'class': 'btn btn-sm btn-outline-secondary'}))
    dowload_rdiff = forms.FileField(label=_('rdiff склад'), required=False,
                                    widget=forms.ClearableFileInput(
                                        attrs={'class': 'btn btn-sm btn-outline-secondary'}))
    dowload_s = forms.FileField(label=_('s склад'), required=False,
                                widget=forms.ClearableFileInput(
                                    attrs={'class': 'btn btn-sm btn-outline-secondary'}))
    dowload_full = forms.FileField(label=_('Все склады'), required=False,
                                   widget=forms.ClearableFileInput(attrs={'class': 'btn btn-sm btn-outline-secondary'}))

    file = forms.FileField(label=_('Статистика тсд'), required=False,
                           widget=forms.ClearableFileInput(attrs={'class': 'btn btn-sm btn-outline-secondary'}))


class ChoiseTG(forms.Form):
    product = forms.ModelChoiceField(label=_('Товарные группы'), help_text='Группа', required=False,
                                     widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
                                     queryset=choice_groups)
