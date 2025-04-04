import base64
import json
import uuid

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from notifications.signals import notify

from ..models import Message, ChatRoom, User


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for handling real-time chat functionality."""
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

        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name)
        await self.channel_layer.group_add(self.user_group_name,
                                           self.channel_name)

        await self.mark_user_active_in_room(self.room_id, self.user.username)

        await self.accept()

        messages = await self.get_previous_messages()

        if messages:
            sender_ids = {msg.sender_id for msg in messages}
            usernames = await self.get_usernames_bulk(sender_ids)
            profile_pictures = await self.get_profile_pictures_bulk(sender_ids)

            messages_data = [{
                'sender': usernames.get(msg.sender_id, "Unknown"),
                'profile_picture': profile_pictures.get(msg.sender_id, None),
                'message': msg.text,
                'image_url': msg.image.url if msg.image else None,
                'timestamp': msg.timestamp.isoformat()
            } for msg in messages]

            await self.send(
                text_data=json.dumps({'previous_messages': messages_data}))

    async def disconnect(self, close_code):
        """Handles WebSocket disconnection."""
        await self.channel_layer.group_discard(self.room_group_name,
                                               self.channel_name)
        await self.channel_layer.group_discard(self.user_group_name,
                                               self.channel_name)
        await self.mark_user_inactive_in_room(self.room_id, self.user.username)

    async def receive(self, text_data):
        """Handles receiving a message (text or image) from WebSocket."""
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get('message')
        image_data = text_data_json.get('image')

        new_message = None

        if message_text or image_data:
            new_message = await self.save_message(message_text, image_data)

        if new_message:
            sender_username = await self.get_username(new_message.sender_id)
            sender_profile_picture = await self.get_profile_picture(
                new_message.sender_id)
            message_payload = {
                'sender': sender_username,
                'profile_picture': sender_profile_picture,
                'message': new_message.text,
                'image_url': new_message.image.url if new_message.image else None,
                'timestamp': new_message.timestamp.isoformat(),
            }

            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'chat_message', **message_payload}
            )

            other_members = await self.get_other_members()

            for member in other_members:
                user_group = f"user_{member.username.replace(' ', '_')}"
                await self.channel_layer.group_send(
                    user_group,
                    {
                        'type': 'room_preview',
                        'room_id': str(self.chat_room.id),
                        'room_name': self.chat_room.name,
                        'sender': sender_username,
                        'message': message_payload['message'],
                        'timestamp': message_payload['timestamp'],
                        'image_url': message_payload.get('image_url'),
                    }
                )

                is_active = await self.is_user_active_in_room(self.room_id,
                                                              member.username)
                if not is_active:
                    preview = message_text[
                              :100] + "..." if message_text else "Image message"
                    await self.send_notification(member, preview)

    async def chat_message(self, event):
        """Sends a message (text or image) to WebSocket."""
        message_data = {
            'sender': event['sender'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }

        if 'image_url' in event:
            message_data['image_url'] = event['image_url']

        await self.send(text_data=json.dumps(message_data))

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

    @sync_to_async
    def mark_user_active_in_room(self, room_id, username):
        key = f"room_{room_id}_active_users"
        users = set(cache.get(key, []))
        users.add(username)
        cache.set(key, list(users), timeout=3600)

    @sync_to_async
    def mark_user_inactive_in_room(self, room_id, username):
        key = f"room_{room_id}_active_users"
        users = set(cache.get(key, []))
        users.discard(username)
        cache.set(key, list(users), timeout=3600)

    @sync_to_async
    def is_user_active_in_room(self, room_id, username):
        key = f"room_{room_id}_active_users"
        users = cache.get(key, [])
        return username in users

    @sync_to_async
    def get_chat_room(self):
        """Fetches the chat room instance."""
        return ChatRoom.objects.filter(id=self.room_id).first()

    @sync_to_async
    def get_other_members(self):
        """Retrieves a list of other members in the chat room, excluding the current user."""
        return list(self.chat_room.members.exclude(id=self.user.id))

    @sync_to_async
    def get_previous_messages(self):
        """Fetches previous messages for the chat room."""
        return list(Message.objects.filter(chat_room=self.chat_room).order_by(
            '-timestamp')[:50])

    @sync_to_async
    def save_message(self, message_text, image_data):
        """Saves a new message with an optional image."""
        try:
            new_message = Message(chat_room=self.chat_room, sender=self.user,
                                  text=message_text)

            if image_data:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                image_name = f"message_{uuid.uuid4()}.{ext}"
                new_message.image.save(image_name,
                                       ContentFile(base64.b64decode(imgstr)),
                                       save=True)

            new_message.save()
            return new_message

        except Exception as e:
            print(f"[Save Message Error]: {e}")
            return None

    @sync_to_async
    def send_notification(self, recipient, preview):
        """
        Sends a notification to the recipient.
        """
        notify.send(
            sender=self.user,
            recipient=recipient,
            verb='sent you a message',
            description=preview,
            level='chat',
            target=self.chat_room
        )

    @sync_to_async
    def get_username(self, user_id):
        """Fetches a username asynchronously to prevent direct sync access."""
        user = User.objects.filter(id=user_id).first()
        return user.username if user else "Unknown"

    @sync_to_async
    def get_profile_picture(self, user_id):
        """Fetches a profile picture asynchronously to prevent direct sync access."""
        user = User.objects.filter(id=user_id).first()
        return f"{settings.AWS_S3_URL_PROTOCOL}//{settings.AWS_S3_CUSTOM_DOMAIN}/{user.profile_picture}" if user else None

    @sync_to_async
    def get_usernames_bulk(self, user_ids):
        """Fetches usernames for multiple user IDs in bulk."""
        users = User.objects.filter(id__in=user_ids).values_list('id',
                                                                 'username')
        return {user_id: username for user_id, username in users}

    @sync_to_async
    def get_profile_pictures_bulk(self, user_ids):
        """Fetches profile pictures for multiple user IDs in bulk."""
        users = User.objects.filter(id__in=user_ids).values_list('id',
                                                                 'profile_picture')
        return {
            user_id: f"{settings.AWS_S3_URL_PROTOCOL}//{settings.AWS_S3_CUSTOM_DOMAIN}/{profile_picture}" if profile_picture else None
            for user_id, profile_picture in users}
