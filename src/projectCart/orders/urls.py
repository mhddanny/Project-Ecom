from django.urls import path
from . import views

urlpatterns = [
    path('place_older/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    # path('callback/', views.callback, name='callback'),
]