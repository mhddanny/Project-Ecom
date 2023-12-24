from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_admin, name='dashboard_admin'),
    path('admin-profile/', views.profile, name='profile_admin'),

    path('product/', views.product, name='product'),
]