from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/video/(?P<meeting_title>\w+)/$', consumers.VideoChatConsumer.as_asgi()),
]
