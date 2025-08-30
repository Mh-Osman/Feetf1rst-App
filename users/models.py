from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
# Create your models here.
from django.utils import timezone
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)  # ✅ Stores OTP temporarily
    otp_created_at = models.DateTimeField(null=True, blank=True)  # ✅ Track OTP creation time
    date_joined = models.DateTimeField(default=timezone.now)

    # Optional: Add these for better admin interface
    first_name = None  # Explicitly set to None since you're using full_name
    last_name = None   # Explicitly set to None since you're using full_name
    
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'date_of_birth']

    def __str__(self):
        return self.email
    
    #  # Optional: Add this method for Django admin compatibility
    # def get_full_name(self):
    #     return self.full_name
    
    # def get_short_name(self):
    #     return self.full_name.split()[0] if self.full_name else self.email
   
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/',default='profile_pics/default.png', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.full_name}'s Profile"


# class question_2(models.Model):
    
    

#     def __str__(self):
#         return f"{self.user.full_name}'s Answer to Question 2"  
    

class signupOnboarding(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='onboarding')
    
    how_did_you_hear = models.JSONField(blank=True, null=True)  # "Come ha scoperto FeetF1rst?" - can be multiple selections
    favorite_products = models.CharField(max_length=255, blank=True, null=True)  # "Quali sono i prodotti che utilizzi di più?"
    foot_or_shoe_issues = models.CharField(max_length=255, blank=True, null=True)  # "C'è qualcosa riguardo a problemi ai piedi o scarpe non adatte?"
   
    
    def __str__(self):
        return f"{self.user.full_name}'s Onboarding Responses"
    
