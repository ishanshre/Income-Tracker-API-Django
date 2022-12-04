from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from accounts.models import User





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


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    email = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username','password','email','refresh_token', 'access_token']
    
    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed({"error":"Invalid Creditials"})
        if not user.is_active:
            raise AuthenticationFailed({"error":"User is active"})
        tokens = user.get_tokens()
        return {
            'email':user.email,
            'username':user.username,
            'refresh_token':tokens["refresh"],
            'access_token':tokens['access']
        }


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']