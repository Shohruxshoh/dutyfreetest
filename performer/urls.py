from django.urls import path
from .views import ChatNotOrderDeliveryView, ChatMessageGetView, OrderDeliveryView, DeliveryDoneView
from client.views import ChatCreateView, ChatOrderDeliveryGetView, DeliveryEndView

urlpatterns = [
    path('chat-message/<int:pk>', ChatMessageGetView.as_view()),
    path('chat-list-delivery/', ChatNotOrderDeliveryView.as_view()),
    path('order-delivery/', OrderDeliveryView.as_view()),
    path('chat-create/<int:order_id>', ChatCreateView.as_view()),
    path('chat-get/<int:order_id>', ChatOrderDeliveryGetView.as_view()),

    path('order-end-delivery/<int:order_id>/', DeliveryEndView.as_view()),

    path('delivery-done/', DeliveryDoneView.as_view())
]
