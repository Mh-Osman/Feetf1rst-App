from django.shortcuts import render

# Create your views here.
from .models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
from random import randint
import random
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
@api_view(['POST'])
def RegisterView(request):
    if request.method == 'POST':
        if 'email' not in request.data or 'password' not in request.data or 'full_name' not in request.data or 'date_of_birth' not in request.data:
            return Response({"error": "Email, password, full_name, and date_of_birth are required"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": serializer.data,
                "message": "User created successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def LoginView(request):
    if request.method == 'POST':
        if 'email' not in request.data or 'password' not in request.data:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=request.data['email'])
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(request.data['password']):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({"error": "User account is disabled"}, status=status.HTTP_403_FORBIDDEN)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "email": user.email,
                "full_name": user.full_name,
                "date_of_birth": user.date_of_birth,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser
            }
        }, status=status.HTTP_200_OK)
        

@api_view(['POST'])
def VerifyOTPView(request):
    email = request.data.get("email")
    otp = request.data.get("otp")

    if not email or not otp:
        return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "Invalid email."}, status=status.HTTP_404_NOT_FOUND)

    # Check if OTP expired (valid for 5 minutes)
    if user.otp_created_at is None:
        return Response({"error": "OTP not generated. Please register again."}, status=status.HTTP_400_BAD_REQUEST)

    expiry_time = user.otp_created_at + timedelta(minutes=5)
    if timezone.now() > expiry_time:
        return Response({"error": "OTP expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)

    # Check OTP match
    if user.otp != otp:
        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

    # Mark as verified
    user.is_verified = True
    user.otp = None
    user.otp_created_at = None
    user.save()

    return Response({"message": "Account verified successfully."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def ForgotPasswordView(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "No account found with this email."}, status=status.HTTP_404_NOT_FOUND)

    otp = str(random.randint(100000, 999999))
    user.otp = otp
    user.otp_created_at = timezone.now()  # ✅ Set OTP creation time
    user.save()

    send_mail(
        subject="Password Reset OTP",
        message=f"Your OTP for password reset is {otp}. It will expire in 5 minutes.",
        from_email="noreply@yourapp.com",
        recipient_list=[user.email],
    )

    return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def ResetPasswordView(request):
    email = request.data.get("email")
    otp = request.data.get("otp")
    new_password = request.data.get("new_password")
    confirm_password = request.data.get("confirm_password")

    if not all([email, otp, new_password, confirm_password]):
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "Invalid email."}, status=status.HTTP_404_NOT_FOUND)

    # ✅ Check if OTP expired
    if user.otp_created_at is None:
        return Response({"error": "OTP not generated. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)
    
    expiry_time = user.otp_created_at + timedelta(minutes=5)
    if timezone.now() > expiry_time:
        return Response({"error": "OTP expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)

    if user.otp != otp:
        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.otp = None
    user.otp_created_at = None
    user.save()

    return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def ResendOTPView(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "Invalid email."}, status=status.HTTP_404_NOT_FOUND)

    otp = str(random.randint(100000, 999999))
    user.otp = otp
    user.otp_created_at = timezone.now()
    user.save()

    send_mail(
        subject="Your New OTP",
        message=f"Your new OTP is {otp}. It will expire in 5 minutes.",
        from_email="noreply@yourapp.com",
        recipient_list=[user.email],
    )

    return Response({"message": "A new OTP has been sent to your email."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def LogoutView(request):
    try:
        # Get refresh token from request
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()  # Blacklist the refresh token
        return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)