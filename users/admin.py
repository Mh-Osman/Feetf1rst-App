from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Changed from User to CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm,ProfileForm
from .models import Profile
from .models import signupOnboarding
from django.utils.html import format_html
from unfold.admin import ModelAdmin


class CustomUserAdmin(ModelAdmin):
    model = CustomUser

    list_display = ['email', 'full_name', 'is_staff', 'is_active', 'profile_picture_tag']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'date_of_birth')}), 
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'date_of_birth', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'full_name')
    ordering = ('email',)

    # Display profile image from related Profile
    def profile_picture_tag(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            return format_html(
                '<img src="{}" style="width:50px; height:50px; object-fit:cover; border-radius:50%"/>',
                obj.profile.profile_picture.url
            )
        return "-"
    profile_picture_tag.short_description = 'Profile Picture'

admin.site.register(CustomUser, CustomUserAdmin)  # Changed from User to CustomUser


class ProfileAdmin(ModelAdmin):
    model = Profile

    list_display = ['user', 'profile_picture_tag', 'location']  # list view

    # readonly_fields = ['profile_picture_tag']  # show image in detail view

    # Method to display image
    def profile_picture_tag(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width:100px; height:100px; object-fit:cover; border-radius:50%"/>',
                obj.profile_picture.url
            )
        return "-"
    profile_picture_tag.short_description = 'Profile Picture'

admin.site.register(Profile, ProfileAdmin)

class signupOnboardingAdmin(admin.ModelAdmin):
    # Columns in the list view
    list_display = ('id', 'how_did_you_hear_clickable', 'favorite_products', 'foot_or_shoe_issues')
    
    # Make the clickable field read-only
    readonly_fields = ('id','how_did_you_hear_clickable', 'favorite_products', 'foot_or_shoe_issues')
    
    # Hide raw JSON field from admin form
    exclude = ('how_did_you_hear',)

    # Specify order of fields in detail/edit form
    #fields = ('how_did_you_hear_clickable', 'favorite_products', 'foot_or_shoe_issues')

    # Display how_did_you_hear as clickable items
    def how_did_you_hear_clickable(self, obj):
        if obj.how_did_you_hear:
            items = [f'<a href="#">{item}</a>' for item in obj.how_did_you_hear]
            return format_html(", ".join(items))
        return "No Response"
    
    how_did_you_hear_clickable.short_description = "How did you hear about FeetF1rst?"

# Register the model with admin
admin.site.register(signupOnboarding, signupOnboardingAdmin)

from .models import Pdfs
class PdfsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file_link', 'uploaded_at')
    readonly_fields = ('id', 'uploaded_at', 'file_link')

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Download PDF</a>', obj.file.url)
        return "No File"
    file_link.short_description = "PDF File"

admin.site.register(Pdfs, PdfsAdmin)