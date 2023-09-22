from django.urls import path

from authentication.views import UserRegistrationAPIView

from .views import TokenGeneratorVIew

urlpatterns = [
    path("register", UserRegistrationAPIView.as_view()),
    path('token/', TokenGeneratorVIew.as_view()),

]
