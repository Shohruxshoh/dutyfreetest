from django.urls import path
from .views import RegisterView, ChangePasswordView, ResetPasswordRequestView, ResetPasswordConfirmView, ProfileView, \
    ImageAvatarGetView, CountryView, HelpView, LikeView, ReviewView, UserMeView, ReviewGetView, UserMeByIdView, \
    LikeListView
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('user-me/', UserMeView.as_view(), name='user-me'),
    path('user-me/<int:pk>/', UserMeByIdView.as_view(), name='user-me-by-id'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile-country/', CountryView.as_view(), name='profile-country'),
    path('profile-help/', HelpView.as_view(), name='profile-help'),
    path('image-avatar/', ImageAvatarGetView.as_view(), name='image-avatar'),
    path('user-like/<int:pk>/', LikeView.as_view(), name='user-like'),
    path('user-like-list/', LikeListView.as_view(), name='user-like-list'),
    path('reviews/', ReviewGetView.as_view(), name='reviews'),
    path('review-create/<int:user_id>/<int:order_id>', ReviewView.as_view(), name='review-create'),

    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', ResetPasswordRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
]
