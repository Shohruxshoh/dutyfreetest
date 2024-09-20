from django.shortcuts import render, get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from .models import Product, Service, Image, AdditionalInformation, CountryOfOrigin, TypeAlcohol, Category, Brand, \
    SaveProduct
from .serializers import ProductSerializer, ServiceSerializer, ImageSerializer, AdditionalInformationSerializer, \
    CountryOfOriginSerializer, TypeAlcoholSerializer, CategorySerializer, BrandSerializer, SaveProductSerializer, \
    ProductCreateSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from main.paginations import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework import status


# Create your views here.

class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPageNumberPagination


class BrandListView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = CustomPageNumberPagination


class ProductListView(ListAPIView):
    queryset = Product.objects.all().select_related("category", 'brand')
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']


class ProductCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProductCreateSerializer(data=request.data)

        # Validate the data
        if serializer.is_valid():
            # Save the data and create product
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceProductView(APIView):

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('id', OpenApiTypes.INT, OpenApiParameter.PATH, description='product id'),
        ], )
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        queryset = Service.objects.filter(product=product)
        serializer = ServiceSerializer(queryset, many=True)
        return Response(serializer.data)


class ImageProductView(APIView):

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('id', OpenApiTypes.INT, OpenApiParameter.PATH, description='product id'),
        ], )
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        queryset = Image.objects.filter(product=product)
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)


class AdditionalInformationProductView(APIView):

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('id', OpenApiTypes.INT, OpenApiParameter.PATH, description='product id'),
        ], )
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        queryset = AdditionalInformation.objects.filter(product=product)
        serializer = AdditionalInformationSerializer(queryset, many=True)
        return Response(serializer.data)


class CountryOfOriginProductView(ListAPIView):
    queryset = CountryOfOrigin.objects.all()
    serializer_class = CountryOfOriginSerializer
    pagination_class = CustomPageNumberPagination


class TypeAlcoholProductView(ListAPIView):
    queryset = TypeAlcohol.objects.all()
    serializer_class = TypeAlcoholSerializer
    pagination_class = CustomPageNumberPagination


class SaveProductView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('id', OpenApiTypes.INT, OpenApiParameter.PATH, description='product id'),
        ], )
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        if SaveProduct.objects.filter(product=product, user=user).exists():
            return Response({'status': True})
        return Response({'status': False})

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('id', OpenApiTypes.INT, OpenApiParameter.PATH, description='product id'),
        ], )
    def post(self, request, pk, *args, **kwargs):
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        SaveProduct.objects.create(product=product, user=user)
        return Response({'status': True})

    @extend_schema(
        # extra parameters added to the schema

        parameters=[
            OpenApiParameter('id', OpenApiTypes.INT, OpenApiParameter.PATH, description='product id'),
        ], )
    def delete(self, request, pk, *args, **kwargs):
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        save_product = SaveProduct.objects.filter(product=product, user=user)
        for s_p in save_product:
            s_p.delete()
        return Response({'delete': True})


class SaveProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        save_products = SaveProduct.objects.filter(user=user)
        serializer = SaveProductSerializer(save_products, many=True)
        return Response(serializer.data)
