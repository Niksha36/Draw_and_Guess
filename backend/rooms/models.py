from django.db import models
from users.models import User


class Room(models.Model):
    painter = models.ForeignKey(User, related_name='painter_rooms', on_delete=models.CASCADE)
    players = models.ManyToManyField(User, related_name='participating_rooms')
    owner =  models.ForeignKey(User, on_delete=models.CASCADE)
    roomname = models.CharField(max_length=255)
    topic = models.CharField(max_length=255, default='Человек Паук')
    is_private = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    token = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.roomname

