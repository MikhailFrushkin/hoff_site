from django import forms
from django.utils.translation import gettext_lazy as _


class DowloadFileInventory(forms.Form):
    dowload_inventory = forms.FileField(label=_('Файл 6.1'),
                                        widget=forms.ClearableFileInput(
                                            attrs={'class': 'form-control form-control-lg'}))
    dowload_1 = forms.FileField(label=_('Файл просчета'), required=False,
                                widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}))
    dowload_2 = forms.FileField(label=_('Файл просчета'), required=False,
                                widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}))
    dowload_3 = forms.FileField(label=_('Файл просчета'), required=False,
                                widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}))

    def clean_dowload_inventory(self):
        file_xlsx = ['xlsx', 'xls']
        file = self.cleaned_data['dowload_inventory']
        if file:
            if file.name.split('.')[-1] in file_xlsx:
                return file
            else:
                raise forms.ValidationError("Только файлы с расширением: xlsx, xls.")

    def clean_dowload_1(self):
        file_xlsx = ['xlsx', 'xls']
        file = self.cleaned_data['dowload_1']
        if file:
            if file.name.split('.')[-1] in file_xlsx:
                return file
            else:
                raise forms.ValidationError("Только файлы с расширением: xlsx, xls.")

    def clean_dowload_2(self):
        file_xlsx = ['xlsx', 'xls']
        file = self.cleaned_data['dowload_2']
        if file:
            if file.name.split('.')[-1] in file_xlsx:
                return file
            else:
                raise forms.ValidationError("Только файлы с расширением: xlsx, xls.")

    def clean_dowload_3(self):
        file_xlsx = ['xlsx', 'xls']
        file = self.cleaned_data['dowload_3']
        if file:
            if file.name.split('.')[-1] in file_xlsx:
                return file
            else:
                raise forms.ValidationError("Только файлы с расширением: xlsx, xls.")