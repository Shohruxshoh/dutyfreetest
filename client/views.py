from django.shortcuts import render, get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, generics
from users.models import User, CUSTOMER, PERFORMANCE, ADMIN, Country
from users.serializers import UserSerializer
from .consumers import online_users
from .models import Order, ChatMessage, Chat, Delivery, awaiting, completed, progress
from .serializers import OrderSerializer, ChatMessageSerializer, ChatSerializer, DeliverySerializer, \
    OrderUpdateSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from itertools import chain

# Create your views here.

class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class OrderGetUserView(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        # Swagger uchun qo'shimcha parametrlarni aniqlash
        parameters=[
            OpenApiParameter(
                'status',
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description='Filter orders by status (1: В процессе, 2: Ожидает получения, 3: Завершен)',
            ),
        ],
        responses={200: 'Order list', 403: 'Permission denied'},
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == CUSTOMER:
            status_param = request.query_params.get('status', None)
            orders = Order.objects.filter(user=user)

            if status_param:
                orders = orders.filter(status=status_param)

            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)

        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema
        request=OrderSerializer,
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.role == CUSTOMER:
            serializer = OrderSerializer(request.data)
            order = Order.objects.create(user=user, **serializer.data)
            serializer1 = OrderSerializer(order)
            return Response(serializer1.data)
        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)


class OrderUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema
        request=OrderUpdateSerializer,
    )
    def put(self, request, pk, *args, **kwargs):
        user = request.user
        serializer = OrderUpdateSerializer(request.data)
        order = get_object_or_404(Order, pk=pk)
        order.status = serializer.data['status']
        order.save()
        serializer1 = OrderSerializer(order)
        return Response(serializer1.data)


class GetDeliveryView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('username', OpenApiTypes.STR, OpenApiParameter.QUERY, description='username'),
            OpenApiParameter('online', OpenApiTypes.BOOL, OpenApiParameter.QUERY, description='online'),
            OpenApiParameter('directions', OpenApiTypes.STR, OpenApiParameter.QUERY, description='Main directions'),
        ], )
    def get(self, request, *args, **kwargs):
        user = request.user
        username = request.query_params.get('username', None)
        online = request.query_params.get('online', None)
        directions = request.query_params.get('directions', None)
        all_online_users = list(chain(*online_users.values()))
        if user.role in [CUSTOMER, ADMIN]:
            if online:
                if username and directions:
                    users = User.objects.filter(id__in=all_online_users, role=PERFORMANCE, is_active=True,
                                                username__icontains=username,
                                                profile_countries__name__icontains=directions)
                elif username:
                    users = User.objects.filter(id__in=all_online_users, role=PERFORMANCE, is_active=True,
                                                username__icontains=username)
                elif directions:
                    users = User.objects.filter(id__in=all_online_users, role=PERFORMANCE, is_active=True,
                                                profile_countries__name__icontains=directions)
                    print(users)
                else:
                    users = User.objects.filter(id__in=all_online_users, role=PERFORMANCE,
                                                is_active=True, profile_countries__name__icontains=directions)

                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
            else:
                if username and directions:
                    users = User.objects.filter(role=PERFORMANCE, is_active=True,
                                                username__icontains=username, profile_countries__name__icontains=directions)
                elif username:
                    users = User.objects.filter(role=PERFORMANCE, is_active=True,
                                                username__icontains=username)
                elif directions:
                    users = User.objects.filter(role=PERFORMANCE, is_active=True,
                                                profile_countries__name__icontains=directions)
                    print(users)
                else:
                    users = User.objects.filter(role=PERFORMANCE, is_active=True)

                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)

        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)


class GetDeliveryFilterView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        list_country = []
        countries = Country.objects.all()
        for country in countries:
            list_country.append(country.name.upper())
        set_countries = set(list_country)
        return Response({'data': set_countries})


class ChatCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('order_id', OpenApiTypes.INT, OpenApiParameter.PATH, description='order id'),
        ], )
    def post(self, request, order_id, *args, **kwargs):
        user = request.user
        if user.role == PERFORMANCE or user.role == ADMIN:
            chat = Chat.objects.filter(order_id=order_id, delivery_person=user).last()
            if chat:
                serializer = ChatSerializer(chat)
                return Response(serializer.data)
            chat_create = Chat.objects.create(order_id=order_id, delivery_person=user)
            serializer = ChatSerializer(chat_create)
            return Response(serializer.data)
        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)


class UploadFileView(APIView):
    def post(self, request, *args, **kwargs):
        chat_id = request.data.get('chat_id')
        file = request.FILES.get('file')
        chat = Chat.objects.get(id=chat_id)
        chat_message = ChatMessage.objects.create(chat=chat, file=file)
        return Response({'file_url': chat_message.file.url})


class ChatOrderDeliveryGetView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('order_id', OpenApiTypes.INT, OpenApiParameter.PATH, description='order id'),
        ], )
    def get(self, request, order_id, *args, **kwargs):
        user = request.user
        if user.role == PERFORMANCE or user.role == CUSTOMER:
            chat = Chat.objects.filter(order_id=order_id, delivery_person=user).first()
            serializer = ChatSerializer(chat)
            return Response(serializer.data)
        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)


class ChatOrderGetView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('order_id', OpenApiTypes.INT, OpenApiParameter.PATH, description='order id'),
        ], )
    def get(self, request, order_id, *args, **kwargs):
        user = request.user
        if user.role == PERFORMANCE or user.role == CUSTOMER:
            chat = Chat.objects.filter(order_id=order_id)
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


class DeliveryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter('order_id', OpenApiTypes.INT, OpenApiParameter.PATH, description='order id'),
            OpenApiParameter('delivery_id', OpenApiTypes.INT, OpenApiParameter.PATH, description='delivery id'),
        ], )
    def post(self, request, order_id, delivery_id, *args, **kwargs):
        user = request.user
        if user.role == CUSTOMER:
            delivery = Delivery.objects.filter(order_id=order_id, delivery_person_id=delivery_id,
                                               is_accepted=True, is_delivered=False).first()
            order = get_object_or_404(Order, pk=order_id)
            order.status = awaiting
            order.save()
            if delivery:
                serializer = DeliverySerializer(delivery)
                return Response(serializer.data)
            delivery_create = Delivery.objects.create(order_id=order_id, delivery_person_id=delivery_id,
                                                      is_accepted=True)
            serializer = DeliverySerializer(delivery_create)
            return Response(serializer.data)
        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)


class DeliveryEndView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter('order_id', OpenApiTypes.INT, OpenApiParameter.PATH, description='order id'),
        ], )
    def post(self, request, order_id, *args, **kwargs):
        user = request.user
        if user.role == PERFORMANCE:
            delivery = Delivery.objects.filter(order_id=order_id, delivery_person=user,
                                               is_accepted=True, is_delivered=False).first()
            order = get_object_or_404(Order, pk=order_id)
            order.status = completed
            order.save()
            delivery.is_accepted = False
            delivery.is_delivered = True
            delivery.save()
            serializer = DeliverySerializer(delivery)
            return Response(serializer.data)
        return Response({'message': "Вам не разрешено это делать", 'status': False}, status=status.HTTP_403_FORBIDDEN)
