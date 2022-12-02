from rest_framework import serializers
from django.contrib.auth import get_user_model as User

class RegisterUserSerailizer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, min_length=8, write_only=True, style={"input_type":"password"})

    class Meta:
        model = User()
        fields = ['username','email','password']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username','')
        if not username.isalnum():
            raise serializers.ValidationError("The user name should only contain alpha numeric characters")
        return attrs
    
    def create(self, validated_data):
        return User().objects.create_user(**validated_data)
