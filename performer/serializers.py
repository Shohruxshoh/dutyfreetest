from rest_framework import serializers
from .models import ChatMessage, Chat


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')

    class Meta:
        model = ChatMessage
        fields = ['id', 'chat', 'message', 'sender', 'file', 'timestamp']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['sender'] = instance.chat.delivery_person.username
    #     return representation


class ChatSerializer(serializers.ModelSerializer):
    get_last_message = serializers.CharField()

    class Meta:
        model = Chat
        fields = ['id', 'user', 'delivery_person', 'is_not_order', 'timestamp', 'get_last_message']
