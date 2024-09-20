from rest_framework import serializers
from .models import Category, Brand, Product, CountryOfOrigin, TypeAlcohol, AdditionalInformation, Image, Service, \
    SaveProduct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'is_age_limit', 'is_navbar']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    discount_calculation = serializers.CharField(max_length=10, required=False)
    category = serializers.CharField(source='category.title')
    brand = serializers.CharField(source='brand.name')

    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'brand', 'description', 'price', 'currency', 'discount_percent',
                  'is_discount', 'discount_calculation', 'for_whom', 'is_active']


class ProductCreateSerializer(serializers.ModelSerializer):
    for_whom_add = serializers.CharField(max_length=250, allow_null=True, required=False)
    type_vial = serializers.CharField(max_length=250, allow_null=True, required=False)
    aromatic = serializers.CharField(max_length=250, allow_null=True, required=False)
    description_service = serializers.CharField(max_length=1000, allow_null=True, required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = ['title', 'category', 'brand', 'description', 'price', 'currency', 'discount_percent',
                  'is_discount', 'for_whom', 'is_active', 'for_whom_add', 'type_vial',
                  'aromatic', 'description_service', 'image']

    def create(self, validated_data):
        # Additional fields for related models
        for_whom_add = validated_data.pop('for_whom_add', None)
        type_vial = validated_data.pop('type_vial', None)
        aromatic = validated_data.pop('aromatic', None)
        description_service = validated_data.pop('description_service', None)
        image = validated_data.pop('image', None)

        # Create Product object
        product = Product.objects.create(**validated_data)

        # Create related AdditionalInformation object
        AdditionalInformation.objects.create(
            product=product,
            for_whom=for_whom_add,
            type_vial=type_vial,
            aromatic=aromatic
        )

        # Create related Service object
        Service.objects.create(
            product=product,
            description=description_service
        )

        # Create related Image object
        if image:
            Image.objects.create(
                product=product,
                image=image
            )

        return product



class AdditionalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInformation
        fields = ['id', 'for_whom', 'type_vial', 'aromatic']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'description']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class CountryOfOriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryOfOrigin
        fields = ['id', 'country']


class TypeAlcoholSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeAlcohol
        fields = ['id', 'type']


class SaveProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveProduct
        fields = ['id', 'product']
