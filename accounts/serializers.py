from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from accounts.models import User, Profile
from accounts.activation import verify_token



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


class RestPasswordLinkSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ["email",]
    
    def validate(self, attrs):
        try:
            email = attrs.get("email",'')
            if User.objects.filter(email=email).exists():
                return attrs
            else:
                raise serializers.ValidationError({"error":"email does not exists"})
        except:
            pass
        return attrs


class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, style = {"input_style":"password"})
    new_password_confirm = serializers.CharField(write_only=True, style = {"input_style":"password"})
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    class Meta:
        model = User
        fields = [ "new_password", "new_password_confirm", "uidb64","token"]
    

    def validate(self, attrs):
        try:
            new_password = attrs.get("new_password",'')
            new_password_confirm = attrs.get("new_password_confirm",'')
            uidb64 = attrs.get("uidb64", "")
            token = attrs.get("token", "")
            verify_status, uid = verify_token(uidb64=uidb64, token=token, action="reset_password")
            user = User.objects.get(id=uid) or None
            if verify_status and user is not None:
                if new_password and new_password_confirm:
                    if new_password != new_password_confirm:
                        raise serializers.ValidationError(
                            {"error":"password and password confirmation mismatch"}
                        )
                try:
                    validate_password(password=new_password, user=user)
                except ValidationError as e:
                    serializers_error = serializers.as_serializer_error(e)
                    raise serializers.ValidationError(
                        {"password":serializers_error[api_settings.NON_FIELD_ERRORS_KEY]}
                    )
                user.set_password(new_password)
                user.save()
                return user


        except ValidationError as e:
            serializers_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"error":serializers_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        return super().validate(attrs)


class ResendEmailConfirmationLinkSerailizer(serializers.ModelSerializer):
    is_email_confirmed = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ["is_email_confirmed"]


class ResendEmailConfirmationSerilaizer(serializers.ModelSerializer):
    is_email_confirmed = serializers.BooleanField(read_only=True)
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    class Meta:
        model = User
        fields = ["is_email_confirmed", "uidb64","token"]

    def validate(self, attrs):
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')
        verify_status, uid = verify_token(uidb64=uidb64, token=token, action="resend_email_verify")
        if uid is not None and verify_status:
            user = User.objects.get(id=uid)
            user.is_email_confirmed = True
            user.save()
            return user
        return super().validate(attrs)



class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=255, style = {"input_style":"password"})
    new_password = serializers.CharField(max_length=255, style = {"input_style":"password"})
    new_password_confirm = serializers.CharField(max_length=255, style = {"input_style":"password"})

    class Meta:
        model = User
        fields = ["old_password","new_password","new_password_confirm"]
    
    def validate(self, attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.get("new_password_confirm")
        user_id = self.context['user_id']
        user = User.objects.get(id=user_id) or None
        if user is not None:
            if not user.check_password(old_password):
                raise AuthenticationFailed({"error":"old password does not match"})
            if new_password != new_password_confirm:
                raise AuthenticationFailed({"error":"new password and password confirm does not match"})
            user.set_password(new_password)
            user.save()
            return user
        return super().validate(attrs)



class UserDetailSerailaizer(serializers.ModelSerializer):
    is_email_confirmed = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','date_joined','last_login','date_of_birth','is_email_confirmed']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserDetailSerailaizer(read_only=True)
    class Meta:
        model = Profile
        fields = ["user","avatar","bio","phone","twitter","facebook","linkedIn"]


class ProfileEditSerializer(serializers.ModelSerializer):
    user = UserDetailSerailaizer()
    class Meta:
        model = Profile
        fields = ['user','avatar','bio','phone','twitter','facebook','linkedIn']

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        for keys, values in validated_data.items():
            setattr(instance, keys, values)
        user = User.objects.get(profile=instance)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.date_of_birth = user_data.get("date_of_birth", user.date_of_birth)
        user.save()

        instance.save()
        return instance
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("Bad Token")