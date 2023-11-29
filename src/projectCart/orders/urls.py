from django.urls import path
from . import views

urlpatterns = [
    path('place_older/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('payment_midtrants/', views.payment_midtrants, name='payment'),
    path('payment_proses/', views.payment_proses, name='payment_proses'),
    path('order_complete/', views.order_complete, name='order_complete'),
    # path('callback/', views.callback, name='callback'),

    path('my_orders/', views.status_pending, name='my_orders'),
    path('proses/', views.status_proses, name='proses'),
    path('completed/', views.status_comleted, name='completed'),
    path('cencelled/', views.status_cencelled, name='cencelled'),

    path('order_history/<int:order_id>/', views.order_history, name='order_history'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),

    path('my_transaction', views.my_transaction, name='my_transaction'),
]