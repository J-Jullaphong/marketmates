from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from ..models import Forum, Tag


class ForumForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=255,
        required=False,
        help_text="Enter tags separated by commas.",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. trading, investment, หุ้นน่าสนใจ"})
    )

    class Meta:
        model = Forum
        fields = ["title", "description", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter forum title"}),
            "description": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            )
        }

    def clean_tags(self):
        """Sanitize and split tags into a list."""
        tags_input = self.cleaned_data["tags"]
        tags_list = [tag.strip().lower() for tag in tags_input.split(",") if tag.strip()]
        return tags_list  # Return a list of cleaned tag names
