from django.shortcuts import render

from income.models import Income
from income.serilaizer import (
    IncomeViewSerializer,
    IncomeCreateSerializer,
    IncomePatchSerializer,
)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsOwner
# Create your views here.

class IncomeModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ["POST","PUT"]:
            return IncomeCreateSerializer
        elif self.request.method == "PATCH":
            return IncomePatchSerializer
        return IncomeViewSerializer
    
    def get_serializer_context(self):
        return {"owner_id":self.request.user.id}

    