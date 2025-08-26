# forms.py (example)
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser , Profile # Changed from User to CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Changed from User to CustomUser
        fields = ('email', 'full_name', 'date_of_birth')  # Updated field names

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser  # Changed from User to CustomUser
        fields = ('email', 'full_name', 'date_of_birth', 'is_active', 'is_staff', 'is_superuser')  # Updated field names
        
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # Make sure you have a Profile model
        fields = ['profile_picture', 'location']  # Your profile fields