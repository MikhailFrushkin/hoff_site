from django.urls import path
from .views import InventoryPage

app_name = 'inventory'

urlpatterns = [
    path('', InventoryPage.as_view(), name='inventory'),
]
