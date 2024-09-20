from django.contrib import admin
from django_summernote.widgets import SummernoteWidget
from django.db import models
from .models import FAQ, RoadMap, RoadMapRow, LeaveARequest, FAQTwo, Notification, TopSales


class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'created_at', 'updated_at')
    search_fields = ('question', 'answer')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    formfield_overrides = {
        models.TextField: {'widget': SummernoteWidget},
    }

    # Customize the form layout in the admin panel
    fieldsets = (
        (None, {
            'fields': ('question', 'answer')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(FAQ, FAQAdmin)


class FAQTowAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'created_at', 'updated_at')
    search_fields = ('question', 'answer')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    formfield_overrides = {
        models.TextField: {'widget': SummernoteWidget},
    }

    # Customize the form layout in the admin panel
    fieldsets = (
        (None, {
            'fields': ('question', 'answer')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(FAQTwo, FAQTowAdmin)


class LeaveARequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    formfield_overrides = {
        models.TextField: {'widget': SummernoteWidget},
    }

    # Customize the form layout in the admin panel
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(LeaveARequest, LeaveARequestAdmin)


class TopSalesAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'created_at', 'updated_at')
    search_fields = ('title', 'subtitle')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    # Customize the form layout in the admin panel
    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle', 'image', 'url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(TopSales, TopSalesAdmin)

admin.site.register(Notification)
#
# admin.site.register(RoadMapRow)
