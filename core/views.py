from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from core.serializer import (
    ExpenceSerialzer, 
    ExpenceEditSerializer,
    ExpencePatchSerializer,
)
from core.models import Expence
from core.permissions import IsOwner
from core.paginations import CustomDefaultPagination
# Create your views here.


class ExpenceModelViewSet(ModelViewSet):
    queryset = Expence.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = CustomDefaultPagination
    lookup_field = "id"
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return Expence.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ["POST","PUT"]:
            return ExpenceEditSerializer
        elif self.request.method == "PATCH":
            return ExpencePatchSerializer
        return ExpenceSerialzer
