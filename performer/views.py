from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from client.consumers import online_users
from client.serializers import OrderSerializer, DeliverySerializer
from users.models import CUSTOMER, PERFORMANCE
from .models import Chat, ChatMessage
from .serializers import ChatMessageSerializer, ChatSerializer
from client.models import Order, progress, Delivery
from rest_framework.permissions import IsAuthenticated
from itertools import chain

# Create your views here.


class ChatNotOrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('id', OpenApiTypes.INT, OpenApiParameter.PATH, description='delivery id'),
        ], )
    def post(self, request, pk, *args, **kwargs):
        user = request.user
        if user.role == CUSTOMER:
            chat = Chat.objects.filter(user=user, delivery_person_id=pk).last()

            if chat:
                serializer = ChatSerializer(chat)
                return Response(serializer.data)
            chat_create = Chat.objects.create(user=user, delivery_person_id=pk)
            serializer = ChatSerializer(chat_create)
            return Response(serializer.data)
        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)


class ChatNotOrderDeliveryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == PERFORMANCE:
            chat = Chat.objects.filter(delivery_person=user)
            serializer = ChatSerializer(chat, many=True)
            return Response(serializer.data)
        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)


class ChatNotOrderCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == CUSTOMER:
            chat = Chat.objects.filter(user=user)
            serializer = ChatSerializer(chat, many=True)
            return Response(serializer.data)
        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)


class ChatMessageGetView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('id', OpenApiTypes.INT, OpenApiParameter.PATH, description='chat id'),
        ], )
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        if user.role == PERFORMANCE or user.role == CUSTOMER:
            chat_message = ChatMessage.objects.filter(chat_id=pk)
            serializer = ChatMessageSerializer(chat_message, many=True)
            return Response(serializer.data)
        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)


class OrderDeliveryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('online', OpenApiTypes.BOOL, OpenApiParameter.QUERY, description='online'),
            OpenApiParameter('search', OpenApiTypes.STR, OpenApiParameter.QUERY,
                             description='Search by id, delivery, username, or amount'),
            OpenApiParameter('ordering', OpenApiTypes.STR, OpenApiParameter.QUERY,
                             description='Order by amount (asc or desc)'),
        ], )
    def get(self, request, *args, **kwargs):
        user = request.user
        online = request.query_params.get('online', None)
        all_online_users = list(chain(*online_users.values()))
        print(all_online_users)
        if user.role == PERFORMANCE:
            if online:
                orders = Order.objects.filter(user__id__in=all_online_users, status=progress)
                # Get the search query parameter
                search_query = request.query_params.get('search', None)
                # Apply search filter if search query is provided
                if search_query:
                    orders = orders.filter(
                        Q(id__icontains=search_query) |
                        Q(delivery__icontains=search_query) |
                        Q(user__username__icontains=search_query) |
                        Q(amount__icontains=search_query)
                    )
                # Sorting by amount
                ordering = request.query_params.get('ordering', None)
                if ordering == 'asc':
                    orders = orders.order_by('amount')  # Pastdan qimmatga
                elif ordering == 'desc':
                    orders = orders.order_by('-amount')  # Qimmatdan pastga

                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data)
            else:
                orders = Order.objects.filter(status=progress)
                # Get the search query parameter
                search_query = request.query_params.get('search', None)
                # Apply search filter if search query is provided
                if search_query:
                    orders = orders.filter(
                        Q(id__icontains=search_query) |
                        Q(delivery__icontains=search_query) |
                        Q(user__username__icontains=search_query) |
                        Q(amount__icontains=search_query)
                    )
                # Sorting by amount
                ordering = request.query_params.get('ordering', None)
                if ordering == 'asc':
                    orders = orders.order_by('amount')  # Pastdan qimmatga
                elif ordering == 'desc':
                    orders = orders.order_by('-amount')  # Qimmatdan pastga

                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data)
        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)


class DeliveryDoneView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        order = Delivery.objects.filter(delivery_person=user)
        serializer = DeliverySerializer(order, many=True)
        return Response(serializer.data)
