from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Changed from User to CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser  # Changed from User to CustomUser
    
    # Admin list display - fixed field names
    list_display = ['email', 'full_name', 'is_staff', 'is_active']  # Changed 'name' to 'full_name'
    
    # User edit page fields organization - fixed field names
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'date_of_birth')}),  # Changed 'name' to 'full_name', added 'date_of_birth'
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),  # Added 'date_joined'
    )
    
    # New user creation page fields - fixed field names
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'date_of_birth', 'password1', 'password2'),  # Changed 'name' to 'full_name', added 'date_of_birth'
        }),
    )
    
    search_fields = ('email', 'full_name')  # Changed 'name' to 'full_name'
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)  # Changed from User to CustomUser