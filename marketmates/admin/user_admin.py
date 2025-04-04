from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from ..models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for User.
    Shows only essential fields: profile info, join/login activity, no permissions/groups.
    """

    list_display = ('username', 'email', 'display_profile_picture', 'is_active')
    list_filter = ('is_active',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    exclude = ('groups', 'user_permissions', 'is_staff', 'is_superuser')

    fieldsets = (
        ("Authentication Info", {
            'fields': ('username', 'email')
        }),
        ("Personal Info", {
            'fields': ('first_name', 'last_name', 'profile_description', 'profile_picture')
        }),
        ("Status", {
            'fields': ('is_active',)
        }),
        ("Important Dates", {
            'fields': ('last_login', 'date_joined')
        }),
    )

    def display_profile_picture(self, obj):
        """Displays user's profile picture as a small thumbnail."""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return "-"
    display_profile_picture.short_description = "Profile Picture"
