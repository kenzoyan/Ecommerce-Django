
from django.urls import include, path

from . import views
from django.views.generic.base import TemplateView

app_name = 'payment'

urlpatterns = [
    path('', views.BasketView, name='basket'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    
    
]

# path('error/', TemplateView(template_name = 'payment/error.html').as_view(), name='error'),
