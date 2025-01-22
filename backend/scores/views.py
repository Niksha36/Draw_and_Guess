from django.db.models import F
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.models import User
from rooms.models import Room
from scores.models import PlayerScore
from rooms.serializers import RoomSerializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from django.db import transaction
import time
from django.db.utils import OperationalError


class ScoreUpdate(APIView):
    @extend_schema(
        summary="Обновление очков пользователя",
        description="Обновляет очки пользователя в комнате.",
        request={
            "room_id": OpenApiParameter(name="room_id", description="ID комнаты", required=True),
            "token": OpenApiParameter(name="token", description="Токен комнаты", required=True),
            "points": OpenApiParameter(name="points", description="Количество очков для добавления", required=False),
            "increment": OpenApiParameter(name="increment", description="Увеличить количество выигранных игр", required=False)
        },
        responses={
            200: OpenApiResponse(response=RoomSerializers, description="Очки пользователя успешно обновлены"),
            403: OpenApiResponse(description="Нет прав для изменения пользователя"),
            404: OpenApiResponse(description="Пользователь или комната не найдены")
        }
    )
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
            self.update_score(room, points, user)
        if request.data.get("increment"):
            user.winGames += 1
            user.save()

        serializer = RoomSerializers(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_score(self, room, points, user, max_retries=5, delay=0.1):
        retries = 0
        while retries < max_retries:
            try:
                with transaction.atomic():
                    player_score, created = PlayerScore.objects.select_for_update().get_or_create(
                        user=user,
                        room=room,
                        defaults={'score': points}
                    )
                    if not created:
                        player_score.score = F('score') + points
                        player_score.save()
                break
            except OperationalError:
                retries += 1
                time.sleep(delay)
            except IntegrityError:
                with transaction.atomic():
                    player_score = PlayerScore.objects.select_for_update().get(user=user, room=room)
                    player_score.score = F('score') + points
                    player_score.save()
                break