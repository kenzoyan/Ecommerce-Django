from django.shortcuts import redirect
from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('add/', views.add, name='order_add'),

]