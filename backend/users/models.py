from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    winGames = models.IntegerField(default=0)
    # gameScore = models.IntegerField(default=0)
    