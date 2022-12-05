from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin
from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model as User

# Register your models here.


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
