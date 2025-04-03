import logging

from django.views.generic import DetailView
from django.shortcuts import redirect
from django.db.models import Count
from django.utils.text import Truncator
from django.utils.html import strip_tags
from notifications.signals import notify

from ..models import Forum, Comment, Tag, Expert
from ..forms import CommentForm

db_logger = logging.getLogger('db')


class ForumDetailView(DetailView):
    """View for displaying a forum post with its comments."""
    model = Forum
    template_name = "marketmates/forum_detail.html"
    context_object_name = "forum"

    def get_context_data(self, **kwargs):
        """Returns forum details, comments, popular tags and expert, and comment form."""
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(forum=self.object).order_by("created_at")
        context["tags"] = Tag.objects.annotate(forum_count=Count("forum")).order_by("-forum_count")[:5]
        context["form"] = CommentForm()
        context["top_experts"] = Expert.objects.filter(status="Approved").order_by("rank")[:5]
        return context

    def post(self, request, *args, **kwargs):
        """Handles the POST request to add new comment."""
        self.object = self.get_object()
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.forum = self.object
            comment.user = request.user
            comment.save()
            db_logger.info(f"New comment added by {request.user.username} on forum '{self.object.title}'.")
            forum_owner = self.object.created_by

            if forum_owner != request.user:
                clean_comment = strip_tags(comment.comment_content)
                preview = Truncator(clean_comment).chars(150, truncate='...')

                notify.send(
                    sender=request.user,
                    recipient=forum_owner,
                    verb='New Activity',
                    description=f"{request.user.username} replied to your post: {preview}",
                    target=self.object,
                    level='info'
                )

                db_logger.info(f"Notification sent to {forum_owner.username} from {request.user.username} "
                               f"on forum '{self.object.title}'.")

            return redirect("marketmates:forum_detail", pk=self.object.pk)

        db_logger.warning(f"Comment creation failed for user for user {request.user.username} on forum "
                          f"'{self.object.title}'. Errors: {form.errors.as_json()}")
        return self.get(request, *args, **kwargs)
