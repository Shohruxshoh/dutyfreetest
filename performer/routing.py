from django.urls import path
from .consumers import ChatConsumer

websocket_not_order_urlpatterns = [
    path('ws/chat-user/<int:chat_id>/<int:delivery_person_id>/', ChatConsumer.as_asgi()),
]
