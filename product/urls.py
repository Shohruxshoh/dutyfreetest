from django.urls import path
from .views import ProductListView, ServiceProductView, ImageProductView, AdditionalInformationProductView, \
    CountryOfOriginProductView, TypeAlcoholProductView, CategoryListView, BrandListView, SaveProductView, \
    ProductCreateView, SaveProductListView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('category/', CategoryListView.as_view()),
    path('brand/', BrandListView.as_view()),
    path('product-create/', ProductCreateView.as_view()),
    path('service/<int:pk>', ServiceProductView.as_view()),
    path('images/<int:pk>', ImageProductView.as_view()),
    path('additions/<int:pk>', AdditionalInformationProductView.as_view()),
    path('country/', CountryOfOriginProductView.as_view()),
    path('type-alcohol/', TypeAlcoholProductView.as_view()),

    path('save-product/<int:pk>/', SaveProductView.as_view(), name='save-product'),
    path('save-product-list/', SaveProductListView.as_view(), name='save-product-list'),
]
