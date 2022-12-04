from django.db import models
from django.contrib.auth import get_user_model as User
# Create your models here.

class CATEGORY_OPTIONS(models.TextChoices):
    ONLINE_SERVICES = "S", 'Online Services'
    TRAVEL = "T", 'Travel'
    TRANSPORTATION = "Tr"
    FOOD = "F", 'Food'
    INSURANCE = "I",'Insurance'
    ENTERTAINMENT = "E","Entertainment"
    EMERGENCY = "EM", 'Emergency'
    RENT = "R", "Rent"
    UTILIES = "U", "Utilities"
    OTHERS = "O", "Others"

class Expence(models.Model):
    category = models.CharField(max_length=2, choices=CATEGORY_OPTIONS.choices, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    description = models.TextField()
    owner = models.ForeignKey(User(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.username.title()}: {self.amount}"
