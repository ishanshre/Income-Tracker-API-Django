from rest_framework import serializers
from accounts.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.settings import api_settings


class RegisterUserSerailizer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, 
        style={"input_type":"password"},
        # validators=[custom_validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type":"password"})

    class Meta:
        model = User
        fields = ['username','email','password','password2']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username','')
        if not username.isalnum():
            raise serializers.ValidationError("The user name should only contain alpha numeric characters")
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"error":"password doesnot match"})
        user = User(username=username, email=email)
        password = attrs['password']
        try:
            validate_password(password=password, user=user)
        except ValidationError as e:
            serializers_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializers_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class EmailVerifySerializer(serializers.ModelSerializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    class Meta:
        model = User
        fields = ['token', 'uidb64']
