from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_admin, name='dashboard_admin'),
    
    path('orders/', views.orders, name='orders'),

    path('products/', views.products, name='products'),
    path('product-add/', views.add_product, name='add_product'),
    
    path('customers/', views.customers, name='customers'),
    
    path('profile/', views.profile, name='profile'),
    

]