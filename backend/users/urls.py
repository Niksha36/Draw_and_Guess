from django.urls import path
from .views import (UserRegistration, LoginView, 
                    UserListView, UserUpdate)


urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<int:user_id>/update', UserUpdate.as_view(), name='user-update')
]
