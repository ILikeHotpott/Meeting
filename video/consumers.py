from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth import get_user_model
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

User = get_user_model()


class VideoChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.meeting_title = self.scope['url_route']['kwargs']['meeting_title']
        self.room_group_name = f'video_{self.meeting_title}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Add user to Redis set
        user_id = self.scope['user'].id
        redis_client.sadd(f'meeting_{self.meeting_title}_users', user_id)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Remove user from Redis set
        user_id = self.scope['user'].id
        redis_client.srem(f'meeting_{self.meeting_title}_users', user_id)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        # Handle different types of signaling messages
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'signal_message',
                'data': data,
                'sender_channel_name': self.channel_name
            }
        )

    # Receive message from room group
    async def signal_message(self, event):
        data = event['data']
        sender_channel_name = event['sender_channel_name']

        # Send message to WebSocket if not sent by the same user
        if self.channel_name != sender_channel_name:
            await self.send(text_data=json.dumps(data))
