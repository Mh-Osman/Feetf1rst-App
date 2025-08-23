from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
import random
from django.core.mail import send_mail
from django.utils import timezone
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'password', 'confirm_password', 
            'full_name', 'date_of_birth', 'is_active', 
            'is_staff', 'is_superuser'
        )
        read_only_fields = ('id', 'is_active', 'is_staff', 'is_superuser')
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        # Remove confirm_password from validated data
        validated_data.pop('confirm_password')
        
        # Extract password
        password = validated_data.pop('password')
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        
        # Create user
        user = CustomUser(**validated_data)
        user.otp = otp
        user.otp_created_at = timezone.now()  # ✅ Store OTP creation time
        user.is_verified = False
        user.save()
        user.set_password(password)  # This hashes the password
        user.save()
        
        
        # Send OTP via email (assuming email settings are configured)
        send_mail(
            subject="Verify your account from Feetf1rst",
            message=f"Your OTP is {otp}",
            from_email="osmangani1osm@gmail.com",
            #mjuk ubte fhxn gptv 
            recipient_list=[user.email],
        )
        
        return user