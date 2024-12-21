from rest_framework import serializers
from .models import User, Room


class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = {'id', 'name'}


class RoomSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = {'id', 'name'}