from django.core.cache import cache
from django.db.models import Count, Q
from django.utils import timezone
from django.views.generic import TemplateView

from ..models import Forum, Tag, FavoriteForum, Expert
from ..tasks import fetch_and_store_market_data


class HomeView(TemplateView):
    """View for displaying the home page"""
    template_name = "marketmates/home.html"

    def get_context_data(self, **kwargs):
        """Adds forum, top tags and expert to the context."""
        context = super().get_context_data(**kwargs)
        context["forums"] = Forum.objects.all().order_by("-created_at")[:5]
        context["tags"] = Tag.objects.annotate(forum_count=Count("forum")).order_by("-forum_count")[:5]
        first_day_of_month = timezone.now().replace(day=1)
        context["tags"] = Tag.objects.annotate(forum_count=Count("forum")).order_by("-forum_count")[:5]
        context["top_experts"] = (
            Expert.objects.filter(status="Approved")
            .annotate(
                fav_count=Count(
                    'user__forum__favoriteforum',
                    filter=Q(user__forum__favoriteforum__added_at__gte=first_day_of_month)
                )
            )
            .order_by('-fav_count')[:5]
        )
        if self.request.user.is_authenticated:
            favorite_forum_ids = FavoriteForum.objects.filter(user=self.request.user).values_list("forum_id", flat=True)
            context["favorite_forum_ids"] = list(favorite_forum_ids)
        else:
            context["favorite_forum_ids"] = []
        try:
            context.update(cache.get('market_data'))
        except TypeError:
            context.update(fetch_and_store_market_data())

        return context
