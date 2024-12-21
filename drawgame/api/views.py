from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerilizer, RoomSerilizer


class UserView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, world!'})


class RoomView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, world!'})
        
