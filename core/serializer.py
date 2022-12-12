from rest_framework import serializers

from core.models import Expence

from accounts.serializers import SimpleUserSerializer



class ExpenceSerialzer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Expence
        fields = ["id","category","amount","description", "owner", "date","created","updated"]


class ExpenceEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expence
        fields = ["id","category","amount","description","date"]


class ExpencePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expence
        fields = ["id","amount"]