from django.urls import re_path

from app.consumers import AiChatRoomConsumer, MeasurementAlertRoomConsumer

websocket_urlpatterns = [
    re_path(r'^ws/ai-chat/(?P<room_name>[^/]+)/$', AiChatRoomConsumer.as_asgi()),
    re_path(r'^ws/measurement-alerts/(?P<room_name>[^/]+)/$', MeasurementAlertRoomConsumer.as_asgi()),
]
