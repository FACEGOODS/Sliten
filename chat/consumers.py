# chat/consumers.py
import json

from channels.auth import login
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):

        # await login(self.scope, user)
        # # save the session (if the session backend does not access the db you can use `sync_to_async`)
        # await database_sync_to_async(self.scope["session"].save)()

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        name = text_data_json['name']
        message = f'{name} {"(self.room_name)"}: {message}'
        send_to_type = text_data_json['send_to_type']

        if self.room_name == 'A':
            if send_to_type == 'B' or send_to_type == 'BC':
                await self.channel_layer.group_send(
                    'chat_B',
                    {
                        'type': 'chat_message',
                        'message': message
                    }
                )
            if send_to_type == 'C' or send_to_type == 'BC':
                await self.channel_layer.group_send(
                    'chat_C',
                    {
                        'type': 'chat_message',
                        'message': message
                    }
                )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
     