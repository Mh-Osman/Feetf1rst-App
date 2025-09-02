from django.urls import path
from .views import (
    RegisterView,
    VerifyOTPView,
    ResendOTPView,
    ForgotPasswordView,
    ResetPasswordView,
    LoginView,
    LogoutView,  # Imported the LogoutView
    UpdateProfileView , # Imported the UpdateProfileView
    ProfileImageView,
    signupOnboardingview , # Imported the signupOnboardingview]
    PdfsUploadView,  # Imported the PdfsUploadView
)

urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('verify-otp/', VerifyOTPView, name='verify-otp'),
    path('resend-otp/', ResendOTPView, name='resend-otp'),
    path('forgot-password/', ForgotPasswordView, name='forgot-password'),
    path('reset-password/', ResetPasswordView, name='reset-password'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),  # Added logout endpoint
    path('profile/', ProfileImageView, name='profile'),  # Added profile endpoint
    path('profile/update/', UpdateProfileView, name='update-profile'),  # Added profile update endpoint
    path('signuponboarding/', signupOnboardingview, name='onboarding'),  # Added onboarding endpoint
    path('upload-pdf/', PdfsUploadView, name='upload-pdf'),
    
]
