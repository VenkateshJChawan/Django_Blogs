from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

# admin.site.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_superuser']
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_superuser', 'date_joined']



admin.site.register(CustomUser, CustomUserAdmin)
