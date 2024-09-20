from django.db import models
from client.models import Order
from users.models import User


# Create your models here.


class Reviews(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name='заказ', on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(User, verbose_name='поставщик', on_delete=models.CASCADE,
                                 related_name='supplier')
    description = models.TextField('Отзыв', null=True, blank=True)
    star = models.PositiveIntegerField('звезда', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Chat(models.Model):
    user = models.ForeignKey(User, related_name='chat_user', on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(User, related_name='delivery_chats_sender',
                                        on_delete=models.CASCADE)  # Yetkazib beruvchi
    is_not_order = models.BooleanField(default=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def get_last_message(self):
        message = self.chat_messages.filter().last()
        return message.message

    def __str__(self):
        return f'User: {self.user.username}, Delivery Person: {self.delivery_person.username}'

    class Meta:
        verbose_name = 'Чат 2'
        verbose_name_plural = 'Чат 2'
        unique_together = ['user', 'delivery_person']  # Har bir buyurtma va yetkazib beruvchi uchun alohida chat


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name='chat_messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='chat_senders', on_delete=models.CASCADE)
    message = models.TextField('Сообщение', null=True, blank=True)  # Xabar matni majburiy emas
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)  # Fayl saqlash uchun maydon
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Чат Сообщение 2'
        verbose_name_plural = 'Чат Сообщения 2'

    def __str__(self):
        if self.message:
            return f'{self.chat.id}: {self.message[:20]}'
        else:
            return f'{self.chat.id}: [Файл]'
