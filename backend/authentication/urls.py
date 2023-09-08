from django.urls import path
from authentication.views import UserRegistrationAPIView

urlpatterns = [
    path("register", UserRegistrationAPIView.as_view()),
]
