from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_admin, name='dashboard_admin'),
    
    path('orders/', views.orders, name='orders'),

    path('category/', views.category, name='category'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit-category/<slug>/<int:pk>/', views.edit_category, name='edit_category'),

    path('products/', views.products, name='products'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    
    path('customers/', views.customers, name='customers'),
    
    path('profile/', views.profile, name='profile'),
    

]