from rest_framework import serializers

from income.models import Income
from accounts.serializers import SimpleUserSerializer

from django.contrib.auth import get_user_model as User



class IncomeViewSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer()
    class Meta:
        model = Income
        fields = ["id", "source", "amount", "description", "owner", "created", "updated"]


class IncomeCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Income
        fields = ["id", "source", "amount", "description", "created", "updated"]
    
    def create(self, validated_data):
        owner_id = self.context['owner_id']
        return Income.objects.create(owner_id=owner_id, **validated_data)


class IncomePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id','amount']
    
    