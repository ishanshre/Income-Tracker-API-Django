from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin
from django.contrib.auth import get_user_model as User

from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from accounts.models import Profile

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User())
class UserAdmin(Admin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ['username','email','is_staff']
    fieldsets = Admin.fieldsets + (
        (
            "Additional Info", {
                "fields":("date_of_birth","is_email_confirmed")
            }
        ),
    )
    add_fieldsets = (
        (
            "Create User",
            {
                "classes": ("wide",),
                "fields": ("username","email","password1","password2"),
            }
        ),
    )
    def get_inlines(self, request, obj=None):
        if obj:
            return [ProfileInline]
        return []


