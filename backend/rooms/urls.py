from django.urls import path
from .views import RoomCreating


urlpatterns = [
    path('create/', RoomCreating.as_view(), name='room-create'),
]