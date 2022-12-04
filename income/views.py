from django.shortcuts import render

from income.models import Income
from income.serilaizer import (
    IncomeSerializer,
)

from rest_framework.viewsets import ModelViewSet
# Create your views here.

class IncomeModelViewSet(ModelViewSet):
    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        return IncomeSerializer
