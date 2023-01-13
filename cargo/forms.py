from django import forms
from django.utils.translation import gettext_lazy as _


class DowloadFileCargo(forms.Form):
    dowload_cargo = forms.FileField(label=_('Файл DVL'),
                                    widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}))
    dowload_1 = forms.FileField(label=_('Файл сканирования'), required=False,
                                widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}))
    dowload_2 = forms.FileField(label=_('Файл сканирования'), required=False,
                                widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}))
    dowload_3 = forms.FileField(label=_('Файл сканирования'), required=False,
                                widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}))
    dowload_4 = forms.FileField(label=_('Файл сканирования'), required=False,
                                widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}))
    dowload_5 = forms.FileField(label=_('Файл сканирования'), required=False,
                                widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}))

    def clean_dowload_cargo(self):
        file_xlsx = ['xlsx', 'xls']
        file = self.cleaned_data['dowload_cargo']
        if file:
            if file.name.split('.')[-1] in file_xlsx:
                return file
            else:
                raise forms.ValidationError("Только файлы с расширением: xlsx, xls.")

    def clean_dowload_1(self):
        file_xlsx = ['csv']
        file = self.cleaned_data['dowload_1']
        if file:
            if file.name.split('.')[-1] in file_xlsx:
                return file
            else:
                raise forms.ValidationError("Только файлы с расширением: csv.")

    def clean_dowload_2(self):
        file_xlsx = ['csv']
        file = self.cleaned_data['dowload_2']
        if file:
            if file.name.split('.')[-1] in file_xlsx:
                return file
            else:
                raise forms.ValidationError("Только файлы с расширением: csv.")


    def clean_dowload_3(self):
        file_xlsx = ['csv']
        file = self.cleaned_data['dowload_3']
        if file:
            if file.name.split('.')[-1] in file_xlsx:
                return file
            else:
                raise forms.ValidationError("Только файлы с расширением: csv.")

    def clean_dowload_4(self):
        file_xlsx = ['csv']
        file = self.cleaned_data['dowload_4']
        if file:
            if file.name.split('.')[-1] in file_xlsx:
                return file
            else:
                raise forms.ValidationError("Только файлы с расширением: csv.")


    def clean_dowload_5(self):
        file_xlsx = ['csv']
        file = self.cleaned_data['dowload_5']
        if file:
            if file.name.split('.')[-1] in file_xlsx:
                return file
            else:
                raise forms.ValidationError("Только файлы с расширением: csv.")