from django.urls import path
from .views import UserRegistration, LoginView


urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
]