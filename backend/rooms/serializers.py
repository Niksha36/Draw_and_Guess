from rest_framework import serializers
from .models import Room
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username'] 
    
    
class RoomSerializers(serializers.ModelSerializer):
    players = UserSerializer(many=True)
    
    class Meta:
        model = Room
        fields = ['id', 'roomname', 'painter', 
                  'owner', 'players', 'topic',
                  'is_private']


    def create(self, validated_data):
        players = validated_data.pop('players', [])
        room = Room.objects.create(**validated_data)
        room.players.add(validated_data['owner'])
        return room
    
    