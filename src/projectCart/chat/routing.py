from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer),
    path('ws/<str:room_name>/', consumers.ChatRoomConsumer.as_asgi()),
]