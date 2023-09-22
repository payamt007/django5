import json
from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serilizers import UserLoginSerializer, UserRegistrationSerializer


class UserRegistrationAPIView(APIView):
    """
    APIView for registering new user
    """

    @extend_schema(
        request=UserRegistrationSerializer, summary="Register a new user"
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        old_user_count = User.objects.filter(username=username).count()
        if old_user_count > 0:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        User.objects.create_user(username=username, password=password)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class TokenGeneratorVIew(APIView):

    @extend_schema(summary="Logout a user")
    def get(self, request):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie(key='jwt_token')
        return response

    @extend_schema(request=UserLoginSerializer, summary="Login a user")
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            jwt_token = (jwt.encode({
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "id": user.id
            }, settings.SECRET_KEY, algorithm="HS256"))
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(key='jwt_token', value=str(jwt_token),
                                expires=datetime.now(timezone.utc) + timedelta(days=1),
                                httponly=True)
            return response
        return Response(status=status.HTTP_403_FORBIDDEN)
