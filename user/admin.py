from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 'name', 'blood_group', 
        'is_available', 'is_active', 'is_staff', 'is_superuser' 
    )
    list_filter = ('blood_group', 'is_available', 'is_active')
    search_fields = ('email', 'name', 'phone')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': (
            'name', 'age', 'blood_group', 
            'phone', 'address', 'last_donation_date'
        )}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser', 
            'groups', 'user_permissions'
        )}),
        ('Availability', {'fields': ('is_available',)}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (  # Fixed
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'name', 'age', 'blood_group', 'phone', 'address',
                'is_staff', 'is_superuser' 
            ),
        }),
    )
    
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)