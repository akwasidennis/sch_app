from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ('index_number', 'email', 'course', 'is_staff', 'is_admin', 'is_active', 'last_login', 'date_joined',)
    list_filter = ('index_number', 'email', 'course', 'is_staff', 'is_admin', 'is_active',)
    fieldsets = (
        (None, {'fields': ('index_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_admin', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('index_number', 'password1', 'password2', 'is_staff', 'is_admin', 'is_active',)}
        ),
    )
    search_fields = ('index_number', 'course',)
    ordering = ('index_number',)

admin.site.register(CustomUser, CustomUserAdmin)