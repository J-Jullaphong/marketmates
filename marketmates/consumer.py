import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, ChatRoom, User


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """Handles WebSocket connection."""
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"
        self.user_group_name = f"user_{self.user.username.replace(' ', '_')}"

        self.chat_room = await self.get_chat_room()
        if not self.chat_room:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)

        await self.accept()

        messages = await self.get_previous_messages()

        if messages:
            sender_ids = {msg.sender_id for msg in messages}
            usernames = await self.get_usernames_bulk(sender_ids)

            messages_data = [{
                'sender': usernames.get(msg.sender_id, "Unknown"),
                'message': msg.text,
                'timestamp': msg.timestamp.isoformat()
            } for msg in messages]

            await self.send(text_data=json.dumps({'previous_messages': messages_data}))

    async def disconnect(self, close_code):
        """Handles WebSocket disconnection."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handles receiving a message from WebSocket."""
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get('message')

        if not message_text:
            return

        new_message = await self.save_message(message_text)
        if not new_message:
            return

        sender_username = await self.get_username(new_message.sender_id)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender_username,
                'message': new_message.text,
                'timestamp': new_message.timestamp.isoformat(),
            }
        )

    async def chat_message(self, event):
        """Sends a message to WebSocket."""
        await self.send(text_data=json.dumps({
            'sender': event['sender'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))

    @sync_to_async
    def get_chat_room(self):
        """Fetches the chat room instance."""
        return ChatRoom.objects.filter(id=self.room_id).first()

    @sync_to_async
    def get_previous_messages(self):
        """Fetches previous messages for the chat room."""
        return list(Message.objects.filter(chat_room=self.chat_room).order_by('-timestamp')[:50])

    @sync_to_async
    def save_message(self, message_text):
        """Saves a new message to the database."""
        try:
            return Message.objects.create(chat_room=self.chat_room, sender=self.user, text=message_text)
        except Exception:
            return None

    @sync_to_async
    def get_username(self, user_id):
        """Fetches a username asynchronously to prevent direct sync access."""
        user = User.objects.filter(id=user_id).first()
        return user.username if user else "Unknown"

    @sync_to_async
    def get_usernames_bulk(self, user_ids):
        """Fetches usernames for multiple user IDs in bulk."""
        users = User.objects.filter(id__in=user_ids).values_list('id', 'username')
        return {user_id: username for user_id, username in users}
