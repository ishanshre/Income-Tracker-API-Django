from rest_framework import serializers

from income.models import Income


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ["id", "source","amount","description","owner","created","updated"]