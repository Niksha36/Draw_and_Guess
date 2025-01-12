from django.shortcuts import render
from django.utils.crypto import get_random_string
from .serializers import RoomSerializers
from users.models import User
from .models import Room
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, F
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
import random
    

class RoomCreating(APIView):
    @extend_schema(
        summary="Создание комнаты",
        description="Создаёт комнату.",
        request=RoomSerializers,
        responses={
            201: OpenApiResponse(response=RoomSerializers, description="Комната успешно создана"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def post(self, request):
        serializer = RoomSerializers(data=request.data)
        if serializer.is_valid():
            room = serializer.save()
            room.token = get_random_string(32)
            room.link_token = get_random_string(16)
            room.save()
            return Response({"status": "Room created", "id": room.id, 
                             "token": room.token,
                             "link_token": room.link_token}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RoomUpdate(APIView):
    @extend_schema(
        summary="Обновление темы и приватности комнаты",
        description="Позволяет создателю комнаты изменять тему и приватность.",
        responses={
            200: OpenApiResponse(response=RoomSerializers, description="Комната успешно обновлена"),
            403: OpenApiResponse(description="Нет прав для изменения комнаты или неправильный link токен"),
            404: OpenApiResponse(description="Комната не найдена"),
            400: OpenApiResponse(description="Не указан токен пользователя"),
            422: OpenApiResponse(description="Количество игроков в комнате больше, чем новое значение количества игроков")
        }
    )
    def patch(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
            user_token = request.data.get('user_token')
            
            if user_token is None:
                return Response({"error": "Не указан токен пользователя"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Room.DoesNotExist:
            return Response({"error": "Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)
        
        link_token = request.data.get('link_token')
        if room.is_private and link_token != room.link_token:
            return Response({"error": "Неправильный токен"}, status=status.HTTP_403_FORBIDDEN)
        
        topic = request.data.get('topic')
        is_private = request.data.get('is_private')
        is_active = request.data.get('is_active')
        players = request.data.get('players')
        max_players = request.data.get('max_players')
        
        if players:
            player_ids = [player['id'] for player in players if 'id' in player]
            users_to_add = User.objects.filter(id__in=player_ids)
            
            for user in users_to_add:
                user.gameScore = 0
                user.save()
            
            room.players.add(*player_ids)
            room.save()
            
            serializer = RoomSerializers(room)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if room.owner.token != user_token:
            return Response({"error": "Нет прав для изменения комнаты"}, status=status.HTTP_403_FORBIDDEN)
        
        if max_players is not None:
            max_players = int(max_players)
            current_players_count = room.players.count()
            if max_players < current_players_count:
                return Response(
                    {"error": f"Невозможно установить max_players={max_players}, так как в комнате уже {current_players_count} игроков"},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            room.max_players = max_players
        if topic is not None:
            room.topic = topic
        if is_private is not None:
            room.is_private = is_private
        if is_active is not None:
            room.is_active = is_active

        room.save()
        serializer = RoomSerializers(room)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class OpenRoomList(APIView):
    @extend_schema(
        summary="Получение всех открытых комнат",
        description="Позволяет получить все открытые и не заполненые комнаты.",
        responses={
            200: OpenApiResponse(response=RoomSerializers, description="Открытые комнаты успешно получены"),
            404: OpenApiResponse(description="Ни одна открытая комната не найдена")
        }
    )
    def get(self, request):
        open_rooms = Room.objects.filter(is_active=False)\
                            .filter(is_private=False)\
                            .annotate(current_players_count=Count('players'))\
                            .filter(current_players_count__lt=F('max_players'))

        if open_rooms:
            serializer = RoomSerializers(open_rooms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(None, status=status.HTTP_404_NOT_FOUND)
    
    
class RoomDetail(APIView):
    @extend_schema(
        summary="Получение информации о комнате",
        description="Позволяет получить информацию о комнате (уникальный индификатор, кол-во участников ....).",
        responses={
            200: OpenApiResponse(response=RoomSerializers, description="Информация о комнате получена"),
            404: OpenApiResponse(description="Комната с данным индификатором (id) не была найдена")
        }
    )
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
            serializer = RoomSerializers(room)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"error": "Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)
    

class RoomExit(APIView):
    @extend_schema(
    summary="Выход из комнаты",
    description="Позволяет игроку выйти из комнаты. Если это последний игрок, комната удаляется.",
    responses={
        200: OpenApiResponse(response=RoomSerializers, description="Игрок успешно вышел из комнаты"),
        204: OpenApiResponse(description="Комната удалена, так как в ней больше нет игроков"),
        400: OpenApiResponse(description="Не указан id пользователя или его токен"),
        403: OpenApiResponse(description="Неправильный токен пользователя"),
        404: OpenApiResponse(description="Комната или пользователь не найдены")
    }
)
    def patch(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
            user_id = request.data.get('user_id')
            user_token = request.data.get('user_token')
            user = User.objects.get(id=user_id)
            
            if user_id is None or user_token is None:
                return Response({"error": "Не указан user_id или user_token"}, status=status.HTTP_400_BAD_REQUEST)
            elif user_token != user.token:
                return Response({"error": "Неправильный токен пользователя"}, status=status.HTTP_403_FORBIDDEN)
        
        except Room.DoesNotExist:
            return Response({"error": "Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        
        
        if room.painter.id == int(user_id) and room.players.count() > 1:
            players = list(room.players.all())
            current_painter_index = players.index(room.painter) if room.painter in players else -1
            next_painter_index = (current_painter_index + 1) % len(players)  
            room.painter = players[next_painter_index]
            room.save()
                
        room.players.remove(user_id)
        
        if room.players.count() == 0:
            room.delete()
            return Response({"message": "Комната удалена, так как в ней больше нет игроков."}, status=status.HTTP_204_NO_CONTENT)
        
        if room.owner.id == int(user_id):
            if room.players.count() > 0:
                room.owner = room.players.first() 
                room.save()

        serializer = RoomSerializers(room)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RoundUpdate(APIView):
    @extend_schema(
        summary="Обновление раунда",
        description="Обновляет текущего художника в комнате, переходя к следующему игроку.",
        responses={
            200: OpenApiResponse(response=RoomSerializers, description="Раунд успешно обновлён"),
            403: OpenApiResponse(description="Нет прав для изменения раунда"),
            404: OpenApiResponse(description="Комната не найдена")
        }
    )
    def post(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)
        
        token = request.data.get('token')
        if room.token != token: 
            return Response({"error": "Нет прав для изменения раунда"}, status=status.HTTP_403_FORBIDDEN)
              
        players = list(room.players.all())
        current_painter_index = players.index(room.painter) if room.painter in players else -1
        next_painter_index = (current_painter_index + 1) % len(players)  
        room.painter = players[next_painter_index]

        room.save()
        serializer = RoomSerializers(room)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    