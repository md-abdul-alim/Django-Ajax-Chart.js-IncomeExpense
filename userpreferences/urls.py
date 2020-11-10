from . import views
from django.urls import path

urlpatterns = [
    path('currency/', views.currency, name='currency'),
]
