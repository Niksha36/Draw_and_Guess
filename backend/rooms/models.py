from django.db import models
from users.models import User


class Room(models.Model):
    painter = models.ForeignKey(User, related_name='painter_rooms', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='participating_rooms')
    roomname = models.CharField(max_length=255)
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return self.roomname

