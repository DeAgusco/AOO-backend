from django.urls import path
from .views import *

urlpatterns = [
    path('', ClientView.as_view(), name='client'),
]