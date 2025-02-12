from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..models import ChatRoom


@method_decorator(login_required, name="dispatch")
class ChatRoomView(View):

    def get(self, request, room_id, *args, **kwargs):
        room = get_object_or_404(ChatRoom, id=room_id)
        if not room.members.filter(id=self.request.user.id).exists():
            messages.warning(request, 'Sorry, You are not a member of this chat room.')
            return redirect('marketmates:chat_room_list')
        return render(request, 'marketmates/chat_room.html', {
            'room_name': room.name,
            'room_id': room.id,
            'current_user_username': request.user.username
        })
