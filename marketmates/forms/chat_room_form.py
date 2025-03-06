from django import forms
from django.db import transaction
from ..models import ChatRoom, User


class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name', 'capacity']
