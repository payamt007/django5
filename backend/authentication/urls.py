from django.urls import path
from authentication.views import UserRegistrationAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import TokenGeneratorVIew

urlpatterns = [
    path("register", UserRegistrationAPIView.as_view()),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', TokenGeneratorVIew.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
