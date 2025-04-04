from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from ..models import Comment


class CommentForm(forms.ModelForm):
    """A form for creating and editing comments using CKEditor 5."""

    def __init__(self, *args, **kwargs):
        """Initialize the CommentForm."""
        super().__init__(*args, **kwargs)
        self.fields["comment_content"].required = False

    class Meta:
        model = Comment
        fields = ["comment_content"]
        widgets = {
            "comment_content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            )
        }
