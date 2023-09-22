import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication


class CookieAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.COOKIES.get("jwt_token", None)
        if jwt_token:
            user = (jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"]))
            user_object = User(**user)
            if not user_object:
                return None
            return user_object, None
        return None
