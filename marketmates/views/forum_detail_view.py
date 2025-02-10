from django.views.generic import DetailView
from django.shortcuts import redirect
from django.db.models import Count

from ..models import Forum, Comment, Tag
from ..forms import CommentForm


class ForumDetailView(DetailView):
    model = Forum
    template_name = "marketmates/forum_detail.html"
    context_object_name = "forum"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(forum=self.object).order_by("-created_at")
        context["tags"] = Tag.objects.annotate(
            forum_count=Count("forum")
        ).order_by("-forum_count")[:5]
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.forum = self.object
            comment.user = request.user
            comment.save()
            return redirect("marketmates:forum_detail", pk=self.object.pk)

        return self.get(request, *args, **kwargs)
