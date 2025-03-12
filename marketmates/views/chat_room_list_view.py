import json
from operator import attrgetter
from django.utils.timezone import now
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from ..models import ChatRoom, Message
from ..forms import ChatRoomForm

User = get_user_model()


class ChatRoomListView(ListView):
    """View to display a list of chat rooms the user is a member of."""
    model = ChatRoom
    template_name = 'marketmates/chat_room_list.html'
    context_object_name = 'chatrooms'

    def get_queryset(self):
        """Fetches the chat rooms where the current user is a member."""
        return ChatRoom.objects.filter(members=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the template, including:
            - The chat room creation form
            - A list of users (excluding the current user and staff)
            - The last message for each chat room
        """
        context = super().get_context_data(**kwargs)
        context['form'] = ChatRoomForm()

        users = User.objects.exclude(id=self.request.user.id).exclude(is_staff=True)
        context['users_json'] = json.dumps([
            {"id": str(user.id), "username": user.username} for user in users
        ])
        last_messages = list(Message.objects.order_by('chat_room', '-timestamp').distinct('chat_room'))
        last_messages.sort(key=attrgetter('timestamp'), reverse=True)
        context['last_messages'] = last_messages
        context['today_date'] = now().date().strftime("%Y-%m-%d")

        return context

    def post(self, request, *args, **kwargs):
        """Handles chat room creation and member addition when a POST request is made."""
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            chatroom = form.save()

            members_str = request.POST.get('members', '')
            member_ids = members_str.split(',') if members_str else []
            print(member_ids)

            members = User.objects.filter(id__in=member_ids)

            for member in members:
                chatroom.members.add(member)

            chatroom.members.add(self.request.user)
            return redirect('marketmates:chat_room_list')

        return redirect('marketmates:chat_room_list')
