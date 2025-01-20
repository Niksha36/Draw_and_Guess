from django.urls import path
from .views import (RoomCreating, RoomUpdate, OpenRoomList,
                    RoomDetail, RoomExit, RoundUpdate)


urlpatterns = [
    path('create/', RoomCreating.as_view(), name='room-create'),
    path('room/<int:room_id>/update/', RoomUpdate.as_view(), name='room-update'),
    path('room/open/', OpenRoomList.as_view(), name='open-room-list'),
    path('room/<int:room_id>/', RoomDetail.as_view(), name='room-detail'),
    path('room/<int:room_id>/exit/', RoomExit.as_view(), name='exit-room'),
    path('room/<int:room_id>/round/', RoundUpdate.as_view(), name='update-round'),
]