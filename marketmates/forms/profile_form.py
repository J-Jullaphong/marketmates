from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.html import escape
from ..models import User


class ProfileForm(forms.ModelForm):
    """Form for updating user profile information with enhanced validation and input escaping."""
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Current Password',
            'class': 'form-control'
        }),
        required=False
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'New Password',
            'class': 'form-control'
        }),
        required=False,
        validators=[validate_password]
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm New Password',
            'class': 'form-control'
        }),
        required=False,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_description', 'profile_picture']
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'profile_description': 'Profile Description',
            'profile_picture': 'Profile Picture',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'profile_description': forms.Textarea(attrs={'placeholder': 'Profile Description', 'rows': 3}),
            'profile_picture': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs["class"] = "form-control"

        self.fields['email'].required = True
        self.fields['username'].required = True

    def clean_email(self):
        """Validate and escape the email address."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already in use.")
        return escape(email)

    def clean_username(self):
        """Validate and escape the username."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This username is already in use.")
        return escape(username)

    def clean(self):
        """Perform cross-field validation and escape all string inputs."""
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if current_password:
            user = authenticate(username=self.instance.username, password=current_password)
            if not user:
                raise ValidationError("The current password is incorrect.")

        if new_password1 or new_password2:
            if new_password1 != new_password2:
                raise ValidationError("The new passwords do not match.")

        for field_name, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field_name] = escape(value)

        return cleaned_data

    def save(self, commit=True):
        """Save the user profile with updated password and email."""
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password1')

        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()

        return user
