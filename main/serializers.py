from rest_framework import serializers
from .models import FAQ, FAQTwo, LeaveARequest, RoadMap, RoadMapRow, Notification, TopSales


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']


class FAQTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQTwo
        fields = ['id', 'question', 'answer']


class RoadMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadMap
        fields = ['id', 'q', 'date']


class RoadMapRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadMapRow
        fields = ['id', 'q', 'title']


class LeaveARequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveARequest
        fields = ['id', 'name', 'email', 'message']


class OrderAnalyticsSerializer(serializers.Serializer):
    day = serializers.DateField()
    order_count = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderAnalyticsDateSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'created_at', 'is_read']


class TopSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopSales
        fields = ['id', 'title', 'subtitle', 'image', 'url']
