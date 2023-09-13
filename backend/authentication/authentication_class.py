from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import Token
import jwt
from django.conf import settings
import json


class CookieAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.COOKIES.get("auth", None)
        if jwt_token:
            user = (jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"]))
            user_object = User(**json.loads(user))
            if not user_object:
                return None
            # try:
            #     user = User.objects.get(username=username)
            # except User.DoesNotExist:
            #     raise exceptions.AuthenticationFailed('No such user')
            return user, None
        return None
