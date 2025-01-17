from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.models import User
from rooms.models import Room
from scores.models import PlayerScore
from rooms.serializers import RoomSerializers


class ScoreUpdate(APIView):
    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            room_id = request.data.get('room_id')
            room = Room.objects.get(id=room_id)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        except Room.DoesNotExist:
            return Response({"error": "Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)

        token = request.data.get('token')
        if room.token != token:
            return Response({"error": "Нет прав для изменения пользователя"}, status=status.HTTP_403_FORBIDDEN)

        points = request.data.get("points", 0)
        if points:
            print(user, "add points", points)
            self.update_score(room, points, user)
        if request.data.get("increment"):
            user.winGames += 1
            user.save()

        serializer = RoomSerializers(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_score(self, room, points, user):
        try:
            player_score = PlayerScore.objects.get(user=user, room=room)
        except PlayerScore.DoesNotExist:
            player_score = PlayerScore(user=user, room=room, score=0)
        
        player_score.score += points
        player_score.save()
        