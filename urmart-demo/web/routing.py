from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/web/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/urmart/update/$', consumers.UrmartConsumer.as_asgi()),
    re_path(r'wss/web/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'wss/urmart/update/$', consumers.UrmartConsumer.as_asgi()),
]