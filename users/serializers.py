from rest_framework import serializers
from .models import User, Profile, ImageAvatar, Country, Help, Like
from performer.models import Reviews
from rest_framework.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError({'password': 'Пароли не совпадают.'})

        if User.objects.filter(email=attrs['email']).exists():
            raise ValidationError({'email': 'Этот электронный адрес уже зарегистрирован.'})

        if User.objects.filter(username=attrs['username']).exists():
            raise ValidationError({'username': 'Это имя пользователя уже занято.'})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password1'])
        user.is_active = True  # Agar tasdiqlashsiz faol qilishni xohlasangiz
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Emailning mavjudligini tekshirish
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Profile
        fields = (
            'id', 'username', 'email', 'user', 'first_name', 'last_name', 'phone', 'country', 'city', 'description')


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'country', 'city', 'description')


class ImageAvatarSerializer(serializers.ModelSerializer):
    image = serializers.FileField()

    class Meta:
        model = ImageAvatar
        fields = ['id', 'image']


class ImageAvatarGetSerializer(serializers.Serializer):
    image = serializers.FileField()


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ['id', 'question', 'answer']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user_like', 'is_like']


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'description', 'star']


class ReviewsGetSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Reviews
        fields = ['id', 'username', 'order', 'image', 'description', 'star']

    def get_image(self, obj):
        # Foydalanuvchining birinchi tasvirini qaytaradi, agar tasvir mavjud bo'lsa
        user = obj.user
        image_avatar = user.image_user.first()  # Birinchi tasvirni olish
        if image_avatar and image_avatar.image:
            return image_avatar.image.url  # Agar tasvir bo'lsa, URL qaytarish
        return None  # Tasvir yo'q bo'lsa, None qaytarish


class ImageAvatarUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAvatar
        fields = ['id', 'image']


class UserSerializer(serializers.ModelSerializer):
    get_image = ImageAvatarUserSerializer()
    get_country = CountrySerializer(many=True)
    get_star = serializers.CharField(allow_null=True, max_length=200)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'get_image', 'get_country', 'get_star']
