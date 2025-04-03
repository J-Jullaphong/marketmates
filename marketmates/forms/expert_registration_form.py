from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.html import escape
from ..models import Expert, User


class ExpertRegistrationForm(UserCreationForm):
    """Form for registering experts with a certification file."""
    designation = forms.CharField(
        required=True,
        label="Designation",
        help_text="For example: CFT, CMT, CEWA, etc.",
        widget=forms.TextInput(attrs={'placeholder': 'Designation'})
    )
    document = forms.FileField(
        required=True,
        label="Verification Document/Certificate",
        widget=forms.ClearableFileInput(attrs={'accept': 'application/pdf'})
    )
    usable_password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
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

    def clean_email(self):
        """Validate email format, uniqueness, and escape."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return escape(email)

    def clean_document(self):
        """Ensure that the uploaded file is a PDF."""
        document = self.cleaned_data.get("document")
        if document:
            if document.content_type != "application/pdf":
                raise ValidationError("Only PDF files are allowed.")
        return document

    def save(self, commit=True):
        """Save the expert with inactive status and handle certification."""
        user = super().save(commit=False)
        if commit:
            user.is_active = False
            user.username = f"{self.cleaned_data['first_name']}_{self.cleaned_data['last_name']}"
            user.save()

            Expert.objects.create(user=user,
                                  designation=self.cleaned_data['designation'],
                                  document=self.cleaned_data['document'])

        return user
