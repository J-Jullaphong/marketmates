from django.db.models import Count, Q
from django.views.generic import ListView

from ..models import Forum, Tag, ChatRoom


class ForumListView(ListView):
    model = Forum
    template_name = "marketmates/forum_list.html"
    context_object_name = "forums"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        sort_order = self.request.GET.get("sort", "-created_at")
        queryset = Forum.objects.all().order_by(sort_order)

        if query:
            if query.startswith("#"):
                tag_name = query[1:].strip()
                queryset = queryset.filter(
                    tags__tag_name__icontains=tag_name).distinct()
            else:
                queryset = queryset.filter(Q(title__icontains=query) | Q(
                    description__icontains=query)).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.annotate(
            forum_count=Count("forum")).order_by("-forum_count")[:5]
        context["private_groups"] = ChatRoom.objects.filter(is_public=False)[
                                    :5]
        context["query"] = self.request.GET.get("q", "")
        context["sort_order"] = self.request.GET.get("sort", "-created_at")
        return context
