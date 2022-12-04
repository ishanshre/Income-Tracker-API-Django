from rest_framework import serializers

from core.models import Expence

from accounts.serializers import SimpleUserSerializer



class ExpenceSerialzer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Expence
        fields = ["id","category","amount","description", "owner", "created","updated"]
    