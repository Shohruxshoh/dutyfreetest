from django.contrib import admin
from .models import User, Profile, ImageAvatar, Country, Help, Like
from performer.models import Reviews
from django_summernote.widgets import SummernoteWidget
from django.db import models


# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('role',)
    search_fields = ['username', 'email']


admin.site.register(User, UsersAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'country', 'city')
    search_fields = ['first_name', 'last_name', 'phone', 'country', 'city']


admin.site.register(Profile, ProfileAdmin)


class ImageAvatarAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(ImageAvatar, ImageAvatarAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Country, CountryAdmin)


class HelpAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    search_fields = ['question', 'answer']
    formfield_overrides = {
        models.TextField: {'widget': SummernoteWidget},
    }


admin.site.register(Help, HelpAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_like', 'is_like')


admin.site.register(Like, LikeAdmin)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'supplier', 'description', 'star')


admin.site.register(Reviews, ReviewsAdmin)
