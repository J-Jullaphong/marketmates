from django.urls import re_path, path
from marketmates.consumers import ChatConsumer, UserConsumer


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_id>[a-f0-9\-]+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/user/(?P<username>[^/]+)/$", UserConsumer.as_asgi()),
]
