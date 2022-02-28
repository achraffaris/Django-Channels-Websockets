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
        self.room = None
        self.user = None  # new

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        '''
        # Disconnect if user does not exist or not authenticated
        if not User.objects.filter(id=self.scope['user'].id).exists():
            return
        '''    
        self.user = self.scope['user']
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
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = self.scope['user']
        print(self.scope)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user':'anonym'	
        }))
        '''mysite/
        if not user.is_authenticated:
            models.Message.objects.create(sender="Anonymous",message=message)
        else:
            models.Message.objects.create(sender=user,message=message)
        '''

