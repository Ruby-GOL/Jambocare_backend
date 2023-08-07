from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import *

router = DefaultRouter()
router.register('users', UserModelViewSet, basename='users')
router.register('profiles', UserProfileModelViewSet, basename='profiles')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', UserLoginAPIView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterApi.as_view()),
    path('api/user/', SelfUserAPIView.as_view(), name='user'),
    path('api/profile/', SelfProfileAPIView.as_view(), name='profile'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('api/password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('api/confirmation-email/send/', SendEmailConfirmationTokenAPIView.as_view(),name='send_email_confirmation_api_view'),
    path('api/confirmation-email/confirm/', ConfirmEmailGenericAPIView.as_view(), name='account_confirm_email'),

]