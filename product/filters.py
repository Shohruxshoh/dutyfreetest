from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['category', 'brand', 'is_discount', 'price', 'for_whom', 'type_alcohol', 'country_of_origin']
