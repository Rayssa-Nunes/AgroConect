from django.contrib import admin

from .models import CustomUser, Profile

admin.site.register(CustomUser)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'date_birth', 'phone')