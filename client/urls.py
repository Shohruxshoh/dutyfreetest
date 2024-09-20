from django.urls import path, include
from performer.views import ChatNotOrderCustomerView, ChatNotOrderCreateView
from .views import OrderUpdateView, OrderCreateView, OrderGetUserView, OrderListView, \
    UploadFileView, ChatMessageGetView, ChatOrderGetView, GetDeliveryView, DeliveryCreateView, GetDeliveryFilterView

urlpatterns = [
    path('create-order/', OrderCreateView.as_view()),
    path('order-update/<int:pk>', OrderUpdateView.as_view()),
    path('get-user-order/', OrderGetUserView.as_view()),
    path('delivery/', GetDeliveryView.as_view()),
    path('delivery-filter/', GetDeliveryFilterView.as_view()),
    path('list-order/', OrderListView.as_view()),
    path('chat-create-or-get/<int:pk>', ChatNotOrderCreateView.as_view()),
    path('chat-upload-file/', UploadFileView.as_view()),
    path('chat-list-customer/', ChatNotOrderCustomerView.as_view()),
    path('chat-order/<int:order_id>', ChatOrderGetView.as_view()),
    path('chat-message-order/<int:pk>', ChatMessageGetView.as_view()),

    path('order-create-delivery/<int:order_id>/<int:delivery_id>', DeliveryCreateView.as_view()),
]
