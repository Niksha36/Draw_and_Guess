from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    winGames = models.IntegerField(default=0)
    token = models.CharField(max_length=32, blank=True, null=True)
