from django import forms
from django.contrib.auth.forms import AuthenticationForm

from django.utils.translation import gettext_lazy as _


class UploadFile(forms.Form):
    file = forms.FileField(label=_('Файл'), widget=forms.ClearableFileInput(attrs={'class': 'btn btn-sm btn-outline-secondary'}))