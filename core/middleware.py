import jwt
from django.conf import settings
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from users.models import User  # User modelingizni import qiling
from urllib.parse import parse_qs


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # WebSocket query string'dan tokenni olish
        query_string = parse_qs(scope['query_string'].decode())
        token = scope['query_string']
        # token = query_string.get('token')


        if token:
            try:
                # JWT tokenni decode qilish
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = decoded_data['user_id']

                # Foydalanuvchini olish
                scope['user'] = await get_user(user_id)
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
