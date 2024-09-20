import json
from channels.generic.websocket import AsyncWebsocketConsumer
from client.models import ChatMessage, Chat
from asgiref.sync import sync_to_async

online_users = {}  # Har bir chat uchun onlayn foydalanuvchilarni saqlaymiz


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.delivery_person_id = self.scope['url_route']['kwargs']['delivery_person_id']
        self.chat_group_name = f'chat_{self.order_id}_{self.delivery_person_id}'

        chat1 = await self.get_chat(self.order_id, self.delivery_person_id)
        # Guruhga qo'shilish
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        if chat1:
            # Foydalanuvchini onlayn ro'yxatga qo'shish
            if chat1.id not in online_users:
                online_users[chat1.id] = []
            online_users[chat1.id].append(self.scope['user'].id)

        await self.accept()

    async def disconnect(self, close_code):
        # Guruhdan chiqish
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )
        chat1 = await self.get_chat(self.order_id, self.delivery_person_id)
        if chat1:
            # Foydalanuvchini onlayn ro'yxatdan chiqarish
            if chat1.id in online_users and self.scope['user'].id in online_users[chat1.id]:
                online_users[chat1.id].remove(self.scope['user'].id)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', None)  # Xabar matni
        file_data = text_data_json.get('file', None)  # Fayl ma'lumotlari (agar mavjud bo'lsa)

        # Xabarni saqlash
        chat = await self.get_chat(self.order_id, self.delivery_person_id)
        if file_data:
            # Faylni saqlash (async fayl saqlash usuli ishlatish uchun fayl yuklash texnikasi qo'shilishi kerak)
            chat_message = await self.save_file(file_data, chat, self.scope['user'])
            # chat_message = await sync_to_async(ChatMessage.objects.create)(chat=chat, sender=self.scope['user'],
            #                                                                file=file)
        else:
            chat_message = await sync_to_async(ChatMessage.objects.create)(chat=chat, sender=self.scope['user'],
                                                                           message=message)

        # Xabarni guruhga uzatish
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': chat_message.message,
                'file': file_data,
                'sender': self.scope['user'].username
            }
        )

    async def chat_message(self, event):
        message = event.get('message', None)
        file = event.get('file', None)
        sender = event['sender']

        # Xabarni foydalanuvchilarga yuborish
        await self.send(text_data=json.dumps({
            'message': message,
            'file': file,
            'sender': sender
        }))

    @staticmethod
    async def get_chat(order_id, delivery_person_id):
        # Django ORM'da sinxron operatsiyani asinxron rejimda bajarish
        return await sync_to_async(
            Chat.objects.filter(order_id=order_id, delivery_person_id=delivery_person_id).first)()

    @staticmethod
    async def save_file(file_data, chat, sender):
        # Faylni sinxron kontekstda saqlash
        return await sync_to_async(ChatMessage.objects.create)(chat_id=chat.id, file=file_data,
                                                               sender=sender)
