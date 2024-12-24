from django.shortcuts import render
from .serializers import RoomSerializers
from .models import Room
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
    

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
            return Response({"status": "Room created", "id": room.id}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RoomUpdate(APIView):
    @extend_schema(
        summary="Обновление темы и приватности комнаты",
        description="Позволяет создателю комнаты изменять тему и приватность.",
        responses={
            200: OpenApiResponse(response=RoomSerializers, description="Комната успешно обновлена"),
            403: OpenApiResponse(description="Нет прав для изменения комнаты"),
            404: OpenApiResponse(description="Комната не найдена"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def patch(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)
        
        if len(request.data.get("players", [])) == 0:
            if room.owner.id != int(request.data.get('user_id')):
                return Response({"error": "Нет прав для изменения комнаты"}, status=status.HTTP_403_FORBIDDEN)

        topic = request.data.get('topic')
        is_private = request.data.get('is_private')
        players = request.data.get('players')

        if topic is not None:
            room.topic = topic
        if is_private is not None:
            room.is_private = is_private
        if players:
            player_ids = [player['id'] for player in players if 'id' in player]
            room.players.add(*player_ids) 

        room.save()
        serializer = RoomSerializers(room)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class OpenRoomList(APIView):
    def get(self, request):
        open_room = Room.objects.filter(is_private=False).annotate(num_players=Count('players')).filter(num_players__lt=14).first()
        
        if open_room:
            serializer = RoomSerializers(open_room)
            return Response(serializer.data)
        return Response(None)
    
    
class RoomDetail(APIView):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
            serializer = RoomSerializers(room)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"error": "Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)
    

class RoomExit(APIView):
    def patch(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Комната не найдена"}, status=status.HTTP_404_NOT_FOUND)

        user_id = request.data.get('user_id')
        if user_id is None:
            return Response({"error": "Не указан user_id"}, status=status.HTTP_400_BAD_REQUEST)

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