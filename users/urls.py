from django.urls import path
from .views import (
    RegisterView,
    VerifyOTPView,
    ResendOTPView,
    ForgotPasswordView,
    ResetPasswordView,
    LoginView,
    LogoutView,  # Imported the LogoutView
)

urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('verify-otp/', VerifyOTPView, name='verify-otp'),
    path('resend-otp/', ResendOTPView, name='resend-otp'),
    path('forgot-password/', ForgotPasswordView, name='forgot-password'),
    path('reset-password/', ResetPasswordView, name='reset-password'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),  # Added logout endpoint
]
