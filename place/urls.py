from django.urls import path

from .views import DowloadFile

app_name = 'place'

urlpatterns = [
    path('dowload/', DowloadFile.as_view(), name='place_dowload'),
]
