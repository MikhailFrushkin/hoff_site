from django.urls import path
from .views import StatisticMainPage

app_name = 'statistic'

urlpatterns = [
    path('', StatisticMainPage.as_view(), name='statistic'),
]
