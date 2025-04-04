import json

from channels.generic.websocket import AsyncWebsocketConsumer


class UserConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer that handles real-time user-level notifications for chat room previews."""
    async def connect(self):
        """Handles WebSocket connection."""
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.user_group_name = f"user_{self.user.username.replace(' ', '_')}"
        await self.channel_layer.group_add(self.user_group_name,
                                           self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Handles WebSocket disconnection."""
        await self.channel_layer.group_discard(self.user_group_name,
                                               self.channel_name)

    async def room_preview(self, event):
        """Receives and sends real-time preview data for a chat room message."""
        await self.send(text_data=json.dumps({
            'type': 'room_preview',
            'room_id': event['room_id'],
            'room_name': event['room_name'],
            'sender': event['sender'],
            'message': event['message'],
            'timestamp': event['timestamp'],
            'image_url': event.get('image_url')
        }))
