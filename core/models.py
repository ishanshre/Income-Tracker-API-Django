from django.db import models
from django.contrib.auth import get_user_model as User
# Create your models here.

class CATEGORY_OPTIONS(models.TextChoices):
    ONLINE_SERVICES = "Online Services", 'Online Services'
    TRAVEL = "Travel", 'Travel'
    TRANSPORTATION = "Transportation",'Transporation'
    FOOD = "Food", 'Food'
    INSURANCE = "Insurance",'Insurance'
    ENTERTAINMENT = "Entertainment","Entertainment"
    EMERGENCY = "Emergency", 'Emergency'
    RENT = "Rent", "Rent"
    UTILIES = "Utilities", "Utilities"
    OTHERS = "Others", "Others"

class Expence(models.Model):
    category = models.CharField(max_length=20, choices=CATEGORY_OPTIONS.choices, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    description = models.TextField()
    owner = models.ForeignKey(User(), on_delete=models.CASCADE, related_name="expences")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Expences ---> {self.owner.username.title()} --> {self.category}:- {self.amount}"
