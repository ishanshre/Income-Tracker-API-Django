from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(_("email address"), max_length=255, unique=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_email_confirmed = models.BooleanField(default=False)


