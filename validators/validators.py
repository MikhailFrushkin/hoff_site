from django import forms


def validate_file(value):
    FILE_EXT_WHITELIST = ['xlsx', 'xls']
    if value.name.split('.')[-1] in FILE_EXT_WHITELIST:
        return value
    else:
        raise forms.ValidationError(
            'Неверное расширение файла. Допустымые: xlsx, xls',
            params={'value': value},
        )
