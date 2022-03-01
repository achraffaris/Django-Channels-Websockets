from django.shortcuts import render
from . import models
from django.contrib.auth.models import User

def index(request):
    users = User.objects.all()
    context = {
        'users':users
    }
    return render(request, 'chat/index.html', context)


def room(request, room_name):
    messages = models.Message.objects.all()
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })