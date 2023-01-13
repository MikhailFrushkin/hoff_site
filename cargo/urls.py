from django.urls import path
from .views import CargoPage

app_name = 'cargo'

urlpatterns = [
    path('', CargoPage.as_view(), name='cargo'),
]
