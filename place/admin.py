from django.contrib import admin
from .models import BU, Storage, Products


class BuAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(BU, BuAdmin)


class StorageAdmin(admin.ModelAdmin):
    list_display = ('storage', 'bu')


admin.site.register(Storage, StorageAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['bu', 'storage', 'code', 'place', 'short_name', 'name',
                    'reason_code', 'tn', 'ng', 'provider', 'provider_name',
                    'physical_stocks', 'delivery', 'sales', 'reserved', 'available',
                    'doc_number', 'client_number', 'client', 'week', 'delivery_type']
    list_filter = ['storage']


admin.site.register(Products, ProductAdmin)
