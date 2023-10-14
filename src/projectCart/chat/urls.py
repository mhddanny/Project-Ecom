from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='chat-online'),
    # path('<str:room_name>/', views.room, name='room'),

    path('api/create-room/<str:uuid>/', views.create_room, name='create-room'),
    path('chat-admin/', views.chatAdmin, name='chat-admin'),
    path('chat-admin/<str:uuid>', views.chatAdminRoom, name='chat-admin-room'),
]