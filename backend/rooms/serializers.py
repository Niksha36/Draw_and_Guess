from rest_framework import serializers
from .models import Room

    
class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'roomname', 'painter']


    def create(self, validated_data):
        room = Room.objects.create(**validated_data)
        room.save()
        return room
    
    