from rest_framework.views import APIView
from .serilizers import UserRegistrationSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class UserRegistrationAPIView(APIView):
    """
    APIView for logging and registering new user
    """

    def get(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token = Token.objects.create(user=user)
            return Response(status=status.HTTP_201_CREATED, data={"token": token})
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    # @extend_schema(parameters=[FeedDeleteSerializer])
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        old_user_count = User.objects.filter(username=username).count()
        if old_user_count > 0:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        User.objects.create_user(user=username, password=password)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
