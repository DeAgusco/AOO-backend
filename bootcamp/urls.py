from django.urls import path
from .views import *

urlpatterns = [
    path('', BootcampView.as_view(), name='bootcamp'),
]