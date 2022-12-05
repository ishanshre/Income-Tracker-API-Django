from django.shortcuts import render
from django.urls import reverse


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from accounts.models import User
from accounts.serializers import (
    RegisterUserSerailizer,
    EmailVerifySerializer,
    ResendEmailConfirmationLinkSerailizer,
    ResendEmailConfirmationSerilaizer,
    LoginSerializer,
    RestPasswordLinkSerializer,
    ResetPasswordSerializer,
)
from accounts.activation import create_email, verify
from accounts.renderers import UserRenderer
# Create your views here

class RegisterUserView(generics.GenericAPIView):
    serializer_class = RegisterUserSerailizer
    renderer_classes = (UserRenderer,)
    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_obj = User.objects.get(email=serializer.data['email'])
        create_email(request=request, user=user_obj, action="register")


        return Response({"Done":serializer.data,"message":"Check your email to verify your account"}, status=status.HTTP_201_CREATED)
        

# class RegisterUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = User().objects.all()
#     serializer_class = RegisterUserSerailizer


class EmailVerify(generics.GenericAPIView):
    serializer_class = EmailVerifySerializer
    renderer_classes = (UserRenderer,)
    token_params_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description="Description", type=openapi.TYPE_STRING)
    uid_params_config = openapi.Parameter('uidb64', in_=openapi.IN_QUERY, description="Description", type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_params_config, uid_params_config])
    def get(self, request):
        verify_status = verify(request=request, action="email_verify")
        if verify_status:
            return Response({"success":"email successfully verified"}, status=status.HTTP_201_CREATED)
        return Response({"error":"Invalid link for verification"}, status=status.HTTP_400_BAD_REQUEST)


class ResendEmailVerificationApiView(generics.GenericAPIView):
    serializer_class = ResendEmailConfirmationLinkSerailizer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user,data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.is_email_confirmed:
            create_email(request=request, user=request.user, action="resend_email_verify")
            return Response({"done":"email confirm link has been sent to your mail"}, status=status.HTTP_200_OK)
        return Response({"error":"email already confirmed"})


class ResendEmailConfirmationView(generics.GenericAPIView):
    serializer_class = ResendEmailConfirmationSerilaizer
    
    def patch(self, request, *args, **kwargs):
        serilaizer = self.serializer_class(data=request.data)
        serilaizer.is_valid(raise_exception=True)
        return Response(
            {"done":"email confirmation successfull"},
            status=status.HTTP_200_OK

        )

class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordLinkView(generics.GenericAPIView):
    serializer_class = RestPasswordLinkSerializer
    def post(self, request, *args, **kwargs):
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user_obj = User.objects.get(email=serializer.data['email'])
        except:
            return Response({"error":"email_does not exist"})
        create_email(request=request, user=user_obj, action="reset_password")
        return Response(
            {
                "Done":serializer.data, "message":"check your email to reset the password",
            },
            status=status.HTTP_200_OK
        )


class RestPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
                {"detail":"password change successfull"}, status=status.HTTP_200_OK
            )




    