from django.urls import path
from .views import (UserRegistration, LoginView, UserListView)


urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('users/', UserListView.as_view(), name='user-list'),
]
