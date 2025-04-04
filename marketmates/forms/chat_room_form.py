from django import forms

from ..models import ChatRoom


class ChatRoomForm(forms.ModelForm):
    """Form for creating chat rooms."""

    class Meta:
        model = ChatRoom
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'A name of your chatroom...'}),
        }
