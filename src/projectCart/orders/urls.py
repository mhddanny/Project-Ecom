from django.urls import path
from . import views

urlpatterns = [
    path('place_older/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('payment_midtrants/', views.payment_midtrants, name='payment'),
    path('payment_proses/', views.payment_proses, name='payment_proses'),
    path('order_complete/', views.order_complete, name='order_complete'),
    # path('callback/', views.callback, name='callback'),

    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]