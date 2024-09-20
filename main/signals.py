from django.db.models.signals import post_save
from django.dispatch import receiver
from client.consumers import online_users
from client.models import ChatMessage
from performer.models import Reviews
from users.models import Like
from .models import Notification


# Like bo'lganda signal
@receiver(post_save, sender=Like)
def send_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user_like,
            message=f"{instance.user.username} понравился ваш пост."
        )


# Review bo'lganda signal
@receiver(post_save, sender=Reviews)
def send_review_notification(sender, instance, created, **kwargs):

    if created:

        Notification.objects.create(
            user=instance.supplier,
            message=f"{instance.user.username} оставил отзыв на ваш пост."
        )


# Chat xabar bo'lganda signal
@receiver(post_save, sender=ChatMessage)
def send_chat_notification(sender, instance, created, **kwargs):
    chat_id = instance.chat.id
    receiver = instance.chat.delivery_person  # Yetkazib beruvchi
    receiver_id = receiver.id

    # Foydalanuvchi chatda bo'lsa, bildirishnoma yuborilmaydi
    if chat_id in online_users and receiver_id in online_users[chat_id]:
        return

    if created:
        Notification.objects.create(
            user=receiver,
            message=f"У вас есть новое сообщение от {instance.sender.username}."
        )
