from django.db.models import Count, Q
from django.utils import timezone
from django.views.generic import ListView

from ..models import Forum, Tag, FavoriteForum, Expert


class ForumListView(ListView):
    """View for displaying a list of forums with support for search and sorting."""
    model = Forum
    template_name = "marketmates/forum_list.html"
    context_object_name = "forums"
    paginate_by = 5

    def get_queryset(self):
        """Returns filtered and sorted forums based on search query or tag."""
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
                    description__icontains=query) | Q(
                    created_by__username__icontains=query)).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        """Adds favorite forum, top tags and expert, and sort order to the context."""
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            favorite_forum_ids = FavoriteForum.objects.filter(
                user=self.request.user).values_list("forum_id", flat=True)
            context["favorite_forum_ids"] = list(favorite_forum_ids)
        else:
            context["favorite_forum_ids"] = []

        context["tags"] = Tag.objects.annotate(
            forum_count=Count("forum")).order_by("-forum_count")[:5]
        context["query"] = self.request.GET.get("q", "")
        context["sort_order"] = self.request.GET.get("sort", "-created_at")
        first_day_of_month = timezone.now().replace(day=1)
        context["tags"] = Tag.objects.annotate(
            forum_count=Count("forum")).order_by("-forum_count")[:5]
        context["top_experts"] = (
            Expert.objects.filter(status="Approved")
            .annotate(
                fav_count=Count(
                    'user__forum__favoriteforum',
                    filter=Q(
                        user__forum__favoriteforum__added_at__gte=first_day_of_month)
                )
            )
            .order_by('-fav_count')[:5]
        )
        return context
