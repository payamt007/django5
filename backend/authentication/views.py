from rest_framework.views import APIView
from .serilizers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta, timezone


class UserRegistrationAPIView(APIView):
    """
    APIView for registering new user
    """

    @extend_schema(
        request=UserRegistrationSerializer, description="Register a new user"
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

    def post(self, request):
        print("here")
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        # user = authenticate(username=username, password=password)
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            # login(request, user)
            refresh = RefreshToken.for_user(user)
            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(key='jwt_token', value=str(refresh.access_token),
                                expires=datetime.now(timezone.utc) + timedelta(days=1),
                                httponly=False)
            return response
        return Response(status=status.HTTP_403_FORBIDDEN)
