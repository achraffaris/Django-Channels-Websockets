# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from . import models
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.user = None  # new
        self.sender = None
        self.receiver = None
        self.username = None
        self.room = None
    def connect(self):
        self.sender = self.scope['user']
        self.room_group_name = 'chat_%s' % 15
        # Disconnect if user does not exist or not authenticated
        if not User.objects.filter(id=self.scope['user'].id).exists():
            return
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

       # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.sender = self.scope['user']
        self.type = text_data_json['type']
        if self.type == 'typing_message':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'type_message',
                    'username': self.sender.username
                }
            )
        elif self.type == 'sending_message':
            receiver = text_data_json['receiver']
            message = text_data_json['message']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.sender.username,
                    'receiver':receiver
                }
            )
        elif self.type == 'stop_typing_message':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'stop_typing',
                }
            )
    def stop_typing(self, event):
        self.send(text_data=json.dumps({
            'type':'stop_typing_message'
        }))
    def type_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'username':event['username'],
            'type':'typing_message'
        }))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': event['username'],
            'type':'sending_message'
        }))
        self.receiver = User.objects.get(id=event['receiver'])
        # get or create a room of receiver.id + sender.id
        users = User.objects.filter(id__in=[self.sender.id, self.receiver.id])
        print("receiver == "+str(self.receiver) + " sender == " + str(self.sender))
        rooms = models.Room.objects.get(id=15)
        if (self.sender.id == self.scope['user'].id):
            models.Message.objects.create(room=rooms,
                                        sender=self.sender.username,
                                        message=message)

