from django.contrib import admin
from django_summernote.widgets import SummernoteWidget
from django.db import models
from .models import Category, Brand, Product, Service, Image, AdditionalInformation, TypeAlcohol, CountryOfOrigin, \
    SaveProduct


# Register your models here.


class ServiceAdmin(admin.TabularInline):
    model = Service
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': SummernoteWidget},
    }


class ImageAdmin(admin.TabularInline):
    model = Image


class AdditionalInformationAdmin(admin.TabularInline):
    model = AdditionalInformation


class TypeAlcoholAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type',)


admin.site.register(TypeAlcohol, TypeAlcoholAdmin)


class CountryOfOriginAdmin(admin.ModelAdmin):
    list_display = ('country',)
    search_fields = ('country',)


admin.site.register(CountryOfOrigin, CountryOfOriginAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_age_limit', 'is_navbar')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    # Customize the form layout in the admin panel
    fieldsets = (
        (None, {
            'fields': ('title', 'is_age_limit', 'is_navbar')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Category, CategoryAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    # Customize the form layout in the admin panel
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Brand, BrandAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'brand', 'price', 'currency', 'discount_percent', 'is_discount', 'for_whom', 'is_active')
    search_fields = ('title', 'category', 'brand', 'price', 'currency', 'discount_percent')
    list_filter = ('created_at', 'updated_at', 'category', 'brand')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    formfield_overrides = {
        models.TextField: {'widget': SummernoteWidget},
    }
    inlines = [ImageAdmin, AdditionalInformationAdmin, ServiceAdmin]
    # Customize the form layout in the admin panel
    fieldsets = (
        (None, {
            'fields': (
                'title', 'category', 'brand', 'country_of_origin', 'type_alcohol', 'price', 'currency',
                'discount_percent', 'is_discount', 'description', 'for_whom', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Product, ProductAdmin)


class SaveProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user')
    search_fields = ('product', 'user')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    # Customize the form layout in the admin panel
    fieldsets = (
        (None, {
            'fields': ('product', 'user')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(SaveProduct, SaveProductAdmin)

admin.site.register(Service)
admin.site.register(Image)
admin.site.register(AdditionalInformation)
