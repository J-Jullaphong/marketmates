import logging

from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count

from ..models import Forum, Tag, ChatRoom
from ..forms import ForumForm

db_logger = logging.getLogger('db')


class CreateForumView(LoginRequiredMixin, CreateView):
    """View for creating a new forum post."""
    model = Forum
    template_name = "marketmates/create_forum.html"
    form_class = ForumForm

    def get_context_data(self, **kwargs):
        """Adds popular tags and private chat rooms to the context."""
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.annotate(forum_count=Count("forum")).order_by("-forum_count")[:5]
        context["private_groups"] = ChatRoom.objects.filter(is_public=False)[:5]
        return context

    def get_initial(self):
        """Pre-fills the title field if 'prefill_text' is provided in query string."""
        prefill_text = self.request.GET.get("prefill_text", "")
        return {"title": prefill_text}

    def form_valid(self, form):
        """Saves the forum with the current user and handles tag creation."""
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        tag_names = form.cleaned_data.get("tags", [])
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(tag_name=tag_name)
            self.object.tags.add(tag)
        db_logger.info(f"Forum created by {self.request.user.username}: '{self.object.title}'")
        return redirect("marketmates:home")

    def form_invalid(self, form):
        """Renders the form with validation errors if form is invalid."""
        db_logger.warning(f"Forum creation failed for user {self.request.user.username}. Errors: {form.errors.as_json()}")
        return self.render_to_response(self.get_context_data(form=form))
