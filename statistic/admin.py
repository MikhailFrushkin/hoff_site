from django.contrib import admin
from .models import Statistic


class StatisticAdmin(admin.ModelAdmin):
    list_display = ['id_document', 'name_document', 'type_document', 'sklad', 'created_at', 'finished_at',
                    'status', 'user', ]
    list_filter = ['user', 'type_document']


admin.site.register(Statistic, StatisticAdmin)
