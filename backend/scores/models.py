from django.db import models
from users.models import User
from rooms.models import Room

class PlayerScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} в комнате {self.room.roomname}"
    