from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from core.serializer import ExpenceSerialzer
from core.models import Expence
from core.permissions import IsOwner
# Create your views here.


class ExpenceModelViewSet(ModelViewSet):
    serializer_class = ExpenceSerialzer
    queryset = Expence.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "id"
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return Expence.objects.filter(owner=self.request.user)
