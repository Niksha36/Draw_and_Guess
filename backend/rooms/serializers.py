from rest_framework import serializers
from .models import Room
from users.models import User
from scores.models import PlayerScore
from scores.serializers import PlayerScoreSerializer


class RoomSerializers(serializers.ModelSerializer):
    players = serializers.SerializerMethodField()
    
    class Meta:
        model = Room
        fields = ['id', 'roomname', 'painter', 'owner', 'players', 
                  'max_players', 'topic', 'is_private', 'is_active']

    def get_players(self, obj):
        players = []
        for player in obj.players.all():
            try:
                player_score = PlayerScore.objects.get(user=player, room=obj)
                serialized_score = PlayerScoreSerializer(player_score).data['score']
            except PlayerScore.DoesNotExist:
                serialized_score = 0
            
            players.append({
                'username': player.username,
                'score': serialized_score
            })
            
        return players
    
    def create(self, validated_data):
        players = validated_data.pop('players', [])
        room = Room.objects.create(**validated_data)
        room.players.add(validated_data['owner'])
        return room
