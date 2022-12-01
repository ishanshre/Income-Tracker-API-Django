from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model as User



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User()
        fields = ['username','email']


class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = User()
        fields = ['first_name','last_name','username', 'email','date_of_birth','is_email_confirmed']
    