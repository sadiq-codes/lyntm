from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email", "username", "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("country", "phone_number", "pin",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("country", "phone_number", "pin",)}),)


admin.site.register(CustomUser, CustomUserAdmin)
