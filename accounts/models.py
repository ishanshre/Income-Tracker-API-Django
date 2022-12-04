from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

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