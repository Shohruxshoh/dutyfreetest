from django.db import models
from users.models import User
from PIL import Image

# Create your models here.

to_address = '1'
by_agreement = '2'

DELIVERY = (
    (to_address, 'До адреса'),
    (by_agreement, 'По договорённости')
)

progress = '1'
awaiting = '2'
completed = '3'

STATUS = (
    (progress, 'В процессе'),
    (progress, 'Ожидает получения'),
    (progress, 'Завершен'),
)


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    amount = models.DecimalField('Предлагаемая сумма', max_digits=10, decimal_places=2)
    city = models.CharField('Город', max_length=250, null=True, blank=True)
    street = models.CharField('Улица', max_length=250, null=True, blank=True)
    house = models.CharField('Дом', max_length=250, null=True, blank=True)
    structure = models.CharField('Строение', max_length=250, null=True, blank=True)
    description = models.TextField('Описание заказа', null=True, blank=True)
    delivery = models.CharField('Доставка', max_length=250, choices=DELIVERY, default=by_agreement)
    status = models.CharField('СТАТУС', max_length=250, choices=STATUS, default=progress)
    order_file = models.FileField(upload_to='order_file/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказ'

    def __str__(self):
        return f"{self.delivery}-{self.description}"


class Chat(models.Model):
    order = models.ForeignKey(Order, related_name='chats', on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(User, related_name='delivery_chats',
                                        on_delete=models.CASCADE)  # Yetkazib beruvchi
    is_not_order = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def get_last_message(self):
        message = self.messages.filter().last()
        return message.message

    def __str__(self):
        return f'Order: {self.order.id}, Delivery Person: {self.delivery_person.username}'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чат'
        unique_together = ['order', 'delivery_person']  # Har bir buyurtma va yetkazib beruvchi uchun alohida chat


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='senders', on_delete=models.CASCADE)
    message = models.TextField('Сообщение', null=True, blank=True)  # Xabar matni majburiy emas
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)  # Fayl saqlash uchun maydon
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Чат Сообщение'
        verbose_name_plural = 'Чат Сообщения'

    @property
    def is_image(self):
        try:
            image = Image.open(self.file)
            image.verify()
            return True
        except:
            return False

    def __str__(self):
        if self.message:
            return f'{self.chat.delivery_person.username}: {self.message[:20]}'
        else:
            return f'{self.chat.delivery_person.username}: [Файл]'


class Delivery(models.Model):
    order = models.ForeignKey(Order, related_name='orders', on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(User, related_name='delivery_users',
                                        on_delete=models.CASCADE)
    is_accepted = models.BooleanField('принято', default=False)
    is_delivered = models.BooleanField('доставлено', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} {self.delivery_person}"
