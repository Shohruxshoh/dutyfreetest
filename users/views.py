from django.shortcuts import render, get_object_or_404
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics
from rest_framework.permissions import AllowAny

from main.paginations import CustomPageNumberPagination
from .serializers import RegisterSerializer, ChangePasswordSerializer, PasswordResetSerializer, \
    PasswordResetConfirmSerializer, ProfileSerializer, ImageAvatarSerializer, CountrySerializer, \
    ProfileUpdateSerializer, ImageAvatarGetSerializer, HelpSerializer, LikeSerializer, ReviewsSerializer, \
    UserSerializer, ReviewsGetSerializer
from .models import User, ImageAvatar, Profile, Country, Help, Like
from performer.models import Reviews
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(
                description="Password changed successfully.",
                response=ChangePasswordSerializer
            ),
            400: OpenApiResponse(
                description="Invalid data or old password incorrect."
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Неправильный пароль."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordRequestView(APIView):
    @extend_schema(
        # extra parameters added to the schema
        request=PasswordResetSerializer,
        # parameters=[
        #     PasswordResetSerializer
        # ], )
    )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Email yuborish qismi
            reset_link = f"http://127.0.0.1:8000/api/users/password-reset-confirm/{uid}/{token}/"
            send_mail(
                "Запрос на сброс пароля",
                f"Нажмите на ссылку ниже, чтобы сбросить пароль: {reset_link}",
                'noreply@your-domain.com',
                [email],
                fail_silently=False,
            )

            return Response({"message": "Письмо отправлено"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmView(APIView):
    @extend_schema(
        # extra parameters added to the schema
        request=PasswordResetConfirmSerializer,
        # parameters=[
        #     PasswordResetSerializer
        # ], )
    )
    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
                token_generator = PasswordResetTokenGenerator()

                if not token_generator.check_token(user, token):
                    return Response({"error": "Токен недействителен или срок его действия истек."},
                                    status=status.HTTP_400_BAD_REQUEST)

                user.set_password(serializer.validated_data['new_password'])
                user.save()

                return Response({"message": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({"error": "Пользователь, которого не существует"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.filter(user=user).select_related("user").last()
        if not profile:
            raise NotFound({'message': "Не найдено"})
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @extend_schema(
        # extra parameters added to the schema
        request=ProfileUpdateSerializer,
        # parameters=[
        #     PasswordResetSerializer
        # ], )
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.filter(user=user).select_related("user")
        serializer = ProfileUpdateSerializer(request.data)
        if not profile:
            create = Profile.objects.create(user=user, **serializer.data)
            serializer1 = ProfileSerializer(create)
            return Response(serializer1.data)
        profile.update(**serializer.data)
        serializer1 = ProfileSerializer(profile.last())
        return Response(serializer1.data)


class ImageAvatarGetView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser, FileUploadParser]  # Fayllarni yuklash uchun parser qo'shish

    def get(self, request, *args, **kwargs):
        user = request.user
        image = ImageAvatar.objects.filter(user=user).select_related("user").last()
        if not image:
            raise NotFound({'message': "Не найдено"})
        serializer = ImageAvatarSerializer(image)
        return Response(serializer.data)

    @extend_schema(
        request=ImageAvatarGetSerializer,  # Swagger uchun fayl yuklashni ko'rsatish
        # responses=ImageAvatarSerializer
        # parameters=[
        #     # ImageAvatarGetSerializer,
        #     # OpenApiParameter('image', OpenApiTypes.BINARY,  description='image'),
        # ],
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        image = ImageAvatar.objects.filter(user=user).select_related("user").last()

        serializer = ImageAvatarSerializer(data=request.data)
        if serializer.is_valid():
            if not image:
                create = ImageAvatar.objects.create(user=user, image=request.FILES['image'])
                return Response(ImageAvatarSerializer(create).data, status=201)
            # Mavjud rasmni yangilash
            image.delete()
            image = ImageAvatar.objects.create(user=user, image=request.FILES['image'])
            return Response(ImageAvatarSerializer(image).data, status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        user = request.user
        images = ImageAvatar.objects.filter(user=user).select_related("user")
        for image in images:
            image.delete()

        return Response({"message": 'delete'}, status=204)


class CountryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Country.objects.filter(user=user).select_related("user")
        if not profile:
            raise NotFound({'message': "Не найдено"})
        serializer = CountrySerializer(profile, many=True)
        return Response(serializer.data)

    @extend_schema(
        # extra parameters added to the schema
        request=CountrySerializer,
        # parameters=[
        #     PasswordResetSerializer
        # ], )
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = CountrySerializer(request.data)
        country = Country.objects.create(user=user, **serializer.data)
        serializer = CountrySerializer(country)
        return Response(serializer.data)


class HelpView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get(self, request, *args, **kwargs):
        user = request.user
        help = Help.objects.filter(user=user).select_related("user").order_by('-id')
        if not help:
            raise NotFound({'message': "Не найдено"})
        serializer = HelpSerializer(help, many=True)
        return Response(serializer.data)

    @extend_schema(
        # extra parameters added to the schema
        request=HelpSerializer,
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = HelpSerializer(request.data)
        help = Help.objects.create(user=user, **serializer.data)
        serializer = HelpSerializer(help)
        return Response(serializer.data)


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        like = Like.objects.filter(user=user, user_like_id=pk).last()
        serializer = LikeSerializer(like)
        return Response(serializer.data)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        like = Like.objects.filter(user=user, user_like_id=pk).last()
        if like and like.is_like is True:
            like.is_like = False
            like.save()
            serializer = LikeSerializer(like)
            return Response(serializer.data)
        elif like and like.is_like is False:
            like.is_like = True
            like.save()
            serializer = LikeSerializer(like)
            return Response(serializer.data)
        else:
            like = Like.objects.create(user=user, user_like_id=pk)
            serializer = LikeSerializer(like)
            return Response(serializer.data)


class LikeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        like = Like.objects.filter(user=user)
        serializer = LikeSerializer(like, many=True)
        return Response(serializer.data)


class ReviewGetView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        reviews = Reviews.objects.filter(supplier=user)
        serializer = ReviewsGetSerializer(reviews, many=True)
        print(serializer.data)
        return Response(serializer.data)


class ReviewView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # extra parameters added to the schema
        request=ReviewsSerializer,
    )
    def post(self, request, user_id, order_id, *args, **kwargs):
        user = request.user
        serializer = ReviewsSerializer(request.data)
        review = Reviews.objects.filter(user=user, supplier_id=user_id, order_id=order_id)
        if not review:
            review = Reviews.objects.create(user=user, supplier_id=user_id, order_id=order_id, **serializer.data)
            serializer = ReviewsSerializer(review)
            return Response(serializer.data)

        review.update(**serializer.data)
        serializer = ReviewsSerializer(review.last())
        return Response(serializer.data)


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserMeByIdView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
