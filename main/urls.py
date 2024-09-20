from django.urls import path
from .views import FAQListView, FAQTwoListView, LeaveARequestCreateView, index, OrderAnalyticsView, \
    UnreadNotificationsView, MarkNotificationAsReadView, TopSalesListView

urlpatterns = [
    path('faq/', FAQListView.as_view(), name='faq-list'),
    path('faq-two/', FAQTwoListView.as_view(), name='faq-two-list'),
    path('leave-request/', LeaveARequestCreateView.as_view(), name='leave-create'),
    path('analytics/orders/', OrderAnalyticsView.as_view(), name='order-analytics'),
    path('notifications/unread/', UnreadNotificationsView.as_view(), name='unread-notifications'),
    path('notifications/<int:pk>/mark-as-read/', MarkNotificationAsReadView.as_view(),
         name='mark-notification-as-read'),
    path('top-sales-list', TopSalesListView.as_view()),
    path('index/<pk>', index),
]
