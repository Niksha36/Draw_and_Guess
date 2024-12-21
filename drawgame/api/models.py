from django.db import models


class User(models.Model):
    name = models.CharField(max_length=24)
    

class Room(models.Model):
    name = models.CharField(max_length=20)
    