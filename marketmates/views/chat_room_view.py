import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from notifications.models import Notification

from ..models import ChatRoom, User


class ChatRoomView(LoginRequiredMixin, View):
    """
    View for displaying a specific chat room.
    Shows members, available users to add, and marks related notifications as read.
    """
    def get(self, request, room_id, *args, **kwargs):
        """Returns the chat room page for the given room ID if the user is a member."""
        room = get_object_or_404(ChatRoom, id=room_id)
        if not room.members.filter(id=self.request.user.id).exists():
            messages.warning(request,'Sorry, You are not a member of this chat room.')
            return redirect('marketmates:chat_room_list')

        Notification.objects.filter(
            recipient=request.user,
            unread=True,
            target_object_id=room.id,
        ).mark_all_as_read()

        members = room.members.all()
        users = User.objects.exclude(id__in=members).exclude(is_staff=True)

        return render(request, 'marketmates/chat_room.html', {
            'room_name': room.name,
            'room_id': room.id,
            'current_user_username': request.user.username,
            'members': members,
            'users_json': json.dumps([{"id": str(user.id), "username": user.username} for user in users])
        })


@csrf_exempt
@login_required
def add_members(request, room_id):
    """Method for adding new members to a chat room."""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.members.all():
        return JsonResponse({"success": False, "error": "Permission denied"}, status=403)

    try:
        data = json.loads(request.body)
        member_ids = data.get("members", [])

        users_to_add = User.objects.filter(id__in=member_ids)
        room.members.add(*users_to_add)

        return JsonResponse({"success": True, "added_members": len(users_to_add)})
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON format"}, status=400)


@csrf_exempt
@login_required
def remove_member(request, room_id, user_id):
    """Method for removing a member from a chat room."""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

    room = get_object_or_404(ChatRoom, id=room_id)
    user = get_object_or_404(User, id=user_id)

    if request.user in room.members.all() and user in room.members.all():
        room.members.remove(user)
        return JsonResponse({"success": True, "removed_user": user.username})

    return JsonResponse({"success": False, "error": "Permission denied"}, status=403)
