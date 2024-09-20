from django.contrib import admin
from .models import Order, ChatMessage, Chat, Delivery

# Register your models here.
admin.site.register(Order)
admin.site.register(Chat)
admin.site.register(ChatMessage)
admin.site.register(Delivery)
