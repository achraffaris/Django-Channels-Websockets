from django.shortcuts import render
from . import models
def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    messages = models.Message.objects.all()
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })