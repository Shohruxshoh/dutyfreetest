from rest_framework import permissions
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class RoleBasedPermission(permissions.BasePermission):
    allowed_roles = None  # Set this in your view class

    def has_permission(self, request, view):
        token = request.headers.get('Authorization')
        if not token:
            return False

        # Extract JWT token (usually it's prefixed with "Bearer ")
        try:
            token = token.split(' ')[1]
        except IndexError:
            return False

        try:
            # Decode the token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
            request.user = user

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return False

        # Check if the user's role is in allowed_roles
        if self.allowed_roles and user.role not in self.allowed_roles:
            print("salom")
            return False

        return True
