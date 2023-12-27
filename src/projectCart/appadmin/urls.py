from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_admin, name='dashboard_admin'),
    path('profile/', views.profile, name='profile'),
    path('customers/', views.customers, name='customers'),

    path('product/', views.product, name='product'),
]