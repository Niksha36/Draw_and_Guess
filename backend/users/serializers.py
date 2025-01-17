from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from .models import User

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'winGames']


    def create(self, validated_data):
        user = User.objects.create(
                username=validated_data['username'],
                password=make_password(validated_data['password']),
                token=get_random_string(32)
        )
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Неверный никнейм или пароль.')

        attrs['user'] = user
        return attrs

    