from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView

from users.models import ADMIN
from .paginations import CustomPageNumberPagination
from .models import FAQ, FAQTwo, LeaveARequest, RoadMap, RoadMapRow, Notification, TopSales
from .serializers import FAQSerializer, FAQTwoSerializer, LeaveARequestSerializer, OrderAnalyticsSerializer, \
    OrderAnalyticsDateSerializer, TopSalesSerializer, NotificationSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum
from client.models import Order


# Create your views here.

@extend_schema(
    # extra parameters added to the schema
    description='ВОПРОСЫ-ОТВЕТЫ',
)
class FAQListView(ListAPIView):
    queryset = FAQ.objects.all().order_by('-id')
    serializer_class = FAQSerializer
    pagination_class = CustomPageNumberPagination


@extend_schema(
    # extra parameters added to the schema
    description='ЗАРАБАТЫВАЙТЕ ВМЕСТЕ C DUTY FREE',
)
class FAQTwoListView(ListAPIView):
    queryset = FAQTwo.objects.all().order_by('-id')
    serializer_class = FAQTwoSerializer
    pagination_class = CustomPageNumberPagination


@extend_schema(
    # extra parameters added to the schema
    description='Заинтересовало? Оставьте заявку!',
)
class LeaveARequestCreateView(CreateAPIView):
    queryset = LeaveARequest.objects.all()
    serializer_class = LeaveARequestSerializer


class OrderAnalyticsView(APIView):
    @extend_schema(
        parameters=[OrderAnalyticsDateSerializer],
        responses={200: OrderAnalyticsSerializer(many=True)},
        description="API для получения аналитики заказов (количество заказов и общая сумма за день) в заданном диапазоне дат."
    )
    def get(self, request):
        user = request.user
        # Set date range (you can get this dynamically from request parameters if needed)
        if user.role == ADMIN:
            start_date = request.GET.get('start_date', '2024-05-10')
            end_date = request.GET.get('end_date', '2024-05-30')

            # Query the Order model to count the orders and sum the amounts by date
            orders = Order.objects.filter(
                created_at__date__range=[start_date, end_date]
            ).extra(select={'day': 'date(created_at)'}).values('day').annotate(
                order_count=Count('id'),
                total_amount=Sum('amount')
            )

            # Serialize the result
            serializer = OrderAnalyticsSerializer(orders, many=True)
            return Response(serializer.data)
        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)


class UnreadNotificationsView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Faqat ko'rilmagan (is_read=False) xabarnomalarni qaytaradi
        return Notification.objects.filter(user=self.request.user, is_read=False).order_by('-id')


class MarkNotificationAsReadView(UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        notification = self.get_object()

        # Xabarnomani faqat foydalanuvchi o'z xabarini yangilashi mumkin
        if notification.user != request.user:
            return Response({"detail": "Не имеете права отмечать это уведомление как прочитанное."}, status=403)

        # Xabarni ko'rilgan qilib yangilaymiz
        notification.is_read = True
        notification.save()

        return Response({"detail": "Уведомление отмечено как прочитанное."}, status=200)


class TopSalesListView(ListAPIView):
    queryset = TopSales.objects.all().order_by('-id')
    serializer_class = TopSalesSerializer
    pagination_class = CustomPageNumberPagination


def index(request, pk=None):
    road_map = RoadMap.objects.all()
    road_map_row = RoadMapRow.objects.all()
    if not pk is None:
        road_detail = RoadMap.objects.filter(row_id=pk)
    return render(request, 'index.html',
                  {"road_map": road_map, "road_map_row": road_map_row, "road_detail": road_detail})
