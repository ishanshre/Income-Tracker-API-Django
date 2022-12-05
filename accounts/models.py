from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(_("email address"), max_length=255, unique=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_email_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return self.username

    
    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        tokens = {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }
        return tokens

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="user/profile")
    bio = models.TextField(max_length=1000)
    phone = PhoneNumberField()
    twitter = models.URLField(null=True, blank=True, max_length=255)
    facebook = models.URLField(null=True, blank=True, max_length=255)
    linkedIn = models.URLField(null=True, blank=True, max_length=255)
