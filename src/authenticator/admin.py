from django.contrib import admin
from authenticator.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from authenticator.forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'username',
        'phone_number',
        'is_staff',
        'is_active',
        'is_superuser'
    ]
    fieldsets = [
        [None, {'fields': ['username', 'password']}],
        [
            'Personal Info', {
                'fields': [
                    'first_name', 
                    'last_name',
                    'phone_number', 
                    'dob', 
                    'about',
                    'profile_pic'
                ]
            }
        ],
        [
            'Permissions', {
                'fields': [
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions'
                ]
            }
        ],
        [
            'Important dates', {
                'fields': [
                    'last_login',
                    'date_joined'
                ]
            }
        ]
    ]

admin.site.register(CustomUser, CustomUserAdmin)