from django.shortcuts import render
from django.urls import reverse

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from accounts.models import User
from accounts.serializers import RegisterUserSerailizer
from accounts.activation import activate, verify
# Create your views here

class RegisterUserView(generics.GenericAPIView):
    serializer_class = RegisterUserSerailizer
    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_obj = User.objects.get(email=serializer.data['email'])
        activate(request=request, user=user_obj)


        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

# class RegisterUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = User().objects.all()
#     serializer_class = RegisterUserSerailizer


class EmailVerify(generics.GenericAPIView):
    def get(self, request):
        verify_status = verify(request=request)
        if verify_status:
            return Response({"success":"email successfully verified"}, status=status.HTTP_201_CREATED)
        return Response({"error":"Invalid link for verification"}, status=status.HTTP_400_BAD_REQUEST)