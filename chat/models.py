from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    users = models.ManyToManyField(User)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField(max_length=300)
    sender = models.TextField(max_length=100)
    timestamp = models.DateField(auto_now_add=True)