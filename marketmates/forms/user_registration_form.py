from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.html import escape
from ..models import User


class UserRegistrationForm(UserCreationForm):
    """Form for registering new users."""
    usable_password = None

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        labels = {
            'email': 'Email',
            'username': 'Username'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = True
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs["class"] = "form-control"
        self.fields['password1'].widget.attrs["placeholder"] = "Password"
        self.fields['password2'].widget.attrs["placeholder"] = "Confirm Password"
        self.fields['password2'].label = "Confirm Password"

    def clean_username(self):
        """Validate username uniqueness, and escape."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")
        return escape(username)

    def clean_email(self):
        """Validate email format, uniqueness, and escape."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return escape(email)
