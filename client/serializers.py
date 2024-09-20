from rest_framework import serializers
from .models import Order, ChatMessage, Chat, Delivery


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'amount', 'city', 'street', 'house', 'structure', 'description', 'delivery', 'status',
                  'order_file', 'created_at', 'updated_at']


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


# chat/serializers.py


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')

    class Meta:
        model = ChatMessage
        fields = ['id', 'chat', 'message', 'sender', 'file', 'is_image', 'timestamp']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['sender'] = instance.chat.delivery_person.username
    #     return representation


class ChatSerializer(serializers.ModelSerializer):
    get_last_message = serializers.CharField()

    class Meta:
        model = Chat
        fields = ['id', 'order', 'delivery_person', 'is_not_order', 'timestamp', 'get_last_message']


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'order', 'delivery_person', 'is_accepted', 'is_delivered', 'created_at', 'updated_at']
