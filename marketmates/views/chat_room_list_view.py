import json
import logging

from datetime import datetime, timedelta
from operator import attrgetter

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max, Value
from django.db.models.functions.comparison import Coalesce
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import ListView
from notifications.models import Notification

from ..forms import ChatRoomForm
from ..models import ChatRoom, Message

User = get_user_model()
db_logger = logging.getLogger('db')


class ChatRoomListView(LoginRequiredMixin, ListView):
    """View for displaying a list of chat rooms."""
    model = ChatRoom
    template_name = 'marketmates/chat_room_list.html'
    context_object_name = 'chatrooms'

    def get_queryset(self):
        """Returns chat rooms for the current user, ordered by latest message time."""
        safe_min_datetime = timezone.make_aware(datetime.min + timedelta(days=1))
        return ChatRoom.objects.filter(members=self.request.user) \
            .annotate(latest_message_time=Coalesce(Max('message__timestamp'), Value(safe_min_datetime))) \
            .order_by('-latest_message_time')

    def get_context_data(self, **kwargs):
        """Returns chat rooms for the current user, ordered by latest message time."""
        context = super().get_context_data(**kwargs)
        context['form'] = ChatRoomForm()
        users = User.objects.exclude(id=self.request.user.id).exclude(is_staff=True)
        context['users_json'] = json.dumps([{"id": str(user.id), "username": user.username} for user in users])
        last_messages = list(Message.objects.order_by('chat_room', '-timestamp').distinct('chat_room'))
        last_messages.sort(key=attrgetter('timestamp'), reverse=True)
        context['last_messages'] = last_messages
        context['today_date'] = timezone.now().date().strftime("%Y-%m-%d")
        context['unread_notifications'] = Notification.objects \
            .filter(recipient=self.request.user, unread=True, level='chat') \
            .values('target_object_id').annotate(unread_count=Count('id'))
        return context

    def post(self, request, *args, **kwargs):
        """Handles chat room creation and adds members and creator to the room."""
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            chatroom = form.save()
            members_str = request.POST.get('members', '')
            member_ids = members_str.split(',') if members_str else []
            members = User.objects.filter(id__in=member_ids)
            for member in members:
                chatroom.members.add(member)
            chatroom.members.add(self.request.user)
            db_logger.info(f"Chat room '{chatroom.name}' created by {request.user.username} with members: "
                           f"{[member.username for member in members]}")
            return redirect('marketmates:chat_room_list')

        db_logger.warning(f"Invalid chat room creation attempt by user {request.user.username}")
        return redirect('marketmates:chat_room_list')
