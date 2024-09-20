from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:order_id>/<int:delivery_person_id>/', ChatConsumer.as_asgi()),
]
