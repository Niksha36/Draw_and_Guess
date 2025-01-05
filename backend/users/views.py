from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from .models import User
from .serializers import UserSerializer
from .serializers import LoginSerializer


class UserRegistration(APIView):
    @extend_schema(
        summary="Регистрация пользователя",
        description="Создаёт нового пользователя с уникальным именем.",
        request=UserSerializer,
        responses={
            201: OpenApiResponse(response=UserSerializer, description="Пользователь успешно создан"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"status": "User created", "id": user.id}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    @extend_schema(
        summary="Авторизация пользователя",
        description="Авторизация на сайте.",
        request=LoginSerializer,
        responses={
            201: OpenApiResponse(response=LoginSerializer, description="Успешная авторизация"),
            401: OpenApiResponse(description="Ошибки авторизации")
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({'id': user.id}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
    
class UserListView(APIView):
    @extend_schema(
        summary="Получение списка пользователей",
        description="Возвращает список всех зарегистрированных пользователей.",
        responses={
            200: OpenApiResponse(response=UserSerializer(many=True), description="Список пользователей"),
            404: OpenApiResponse(description="Пользователи не найдены")
        }
    )
    def get(self, request):
        users = User.objects.all() 
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UserUpdate(APIView):
    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.data.get("zeroing"):
            user.gameScore = 0
        if request.data.get("points"):
            points = request.data.get("points", 0)
            user.gameScore += points
        if request.data.get("increment"):
            user.winGames += 1
        
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    