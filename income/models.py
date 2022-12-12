from django.db import models
from django.contrib.auth import get_user_model as User
# Create your models here.

class SOURCE_OPTION(models.TextChoices):
    SALARY = "Salary", 'Salary'
    BUSINESS = "Business", 'Business'
    SIDE_BUSINESS = "Side Business", 'Side Business'
    ROYALTY = "Royalty", 'Royalty'
    RENTAL = "Rental", 'Rental'



class Income(models.Model):
    source = models.CharField(max_length=20, choices=SOURCE_OPTION.choices)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    description = models.TextField()
    owner = models.ForeignKey(User(), on_delete=models.CASCADE, related_name="incomes")
    date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Income --> {self.owner.username.title()} --> {self.source}:- {self.amount}"