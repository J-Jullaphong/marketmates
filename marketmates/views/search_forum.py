from django.views.generic import ListView
from django.db.models import Count

from ..models import Forum, Tag, ChatRoom


class SearchForumView(ListView):
    model = Forum
    template_name = "marketmates/search_result.html"
    context_object_name = "forums"

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        sort_order = self.request.GET.get("sort", "-created_at")

        if query:
            if query.startswith("#"):
                tag_name = query[1:].strip()
                return Forum.objects.filter(tags__tag_name__icontains=tag_name).distinct()
            else:
                return Forum.objects.filter(title__icontains=query).distinct()
        return Forum.objects.all().order_by(sort_order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.annotate(
            forum_count=Count("forum")
        ).order_by("-forum_count")[:5]
        context["private_groups"] = ChatRoom.objects.filter(is_public=False)[:5]
        context["query"] = self.request.GET.get("q", "")
        return context
