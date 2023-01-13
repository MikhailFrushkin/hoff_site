from django.urls import path
from .views import StockPage, DowloadStock, GroupPage

app_name = 'stock'

urlpatterns = [
    path('dowload/', DowloadStock.as_view(), name='stock_dowload'),
    path('<slug:slug>/', GroupPage.as_view(), name='stock_group'),
    path('', StockPage.as_view(), name='stock'),
]
