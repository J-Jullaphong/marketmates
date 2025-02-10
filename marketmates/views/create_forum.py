from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count

from ..models import Forum, Tag, ChatRoom
from ..forms import ForumForm


class CreateForumView(LoginRequiredMixin, CreateView):
    model = Forum
    template_name = "marketmates/create_forum.html"
    form_class = ForumForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.annotate(
            forum_count=Count("forum")
        ).order_by("-forum_count")[:5]
        context["private_groups"] = ChatRoom.objects.filter(is_public=False)[:5]
        return context

    def get_initial(self):
        prefill_text = self.request.GET.get("prefill_text", "")
        return {"title": prefill_text}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        tag_names = form.cleaned_data.get("tags", [])
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(tag_name=tag_name)
            self.object.tags.add(tag)
        return redirect("marketmates:home")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
