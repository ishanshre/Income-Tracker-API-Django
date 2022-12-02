from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model as User


from accounts.serializers import RegisterUserSerailizer
# Create your views here

class RegisterUserView(generics.GenericAPIView):
    serializer_class = RegisterUserSerailizer
    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

# class RegisterUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = User().objects.all()
#     serializer_class = RegisterUserSerailizer