from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    users = models.ManyToManyField(User)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.TextField(default="anonym")
    message = models.TextField(max_length=300)