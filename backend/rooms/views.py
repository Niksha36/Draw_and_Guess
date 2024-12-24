from django.shortcuts import render
from .serializers import RoomSerializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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
    
