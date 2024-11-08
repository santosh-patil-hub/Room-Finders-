# User/admin.py
from django.contrib import admin
from .models import CustomUser,Area,Room

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')


admin.site.register(Area)
admin.site.register(Room)
    