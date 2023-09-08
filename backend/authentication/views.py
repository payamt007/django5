from rest_framework.views import APIView
from .serilizers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema


class UserRegistrationAPIView(APIView):
    """
    APIView for registering new user
    """

    @extend_schema(
        request=UserRegistrationSerializer, description="Register a new user"
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        print("serializr", serializer)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        old_user_count = User.objects.filter(username=username).count()
        if old_user_count > 0:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        User.objects.create_user(username=username, password=password)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
