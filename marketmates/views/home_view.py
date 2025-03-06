from django.core.cache import cache
from django.db.models import Count
from django.views.generic import TemplateView

from ..models import Forum, Tag, ChatRoom
from ..tasks import fetch_and_store_market_data


class HomeView(TemplateView):
    template_name = "marketmates/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forums"] = Forum.objects.all().order_by("-created_at")[:5]
        context["tags"] = Tag.objects.annotate(
            forum_count=Count("forum")
        ).order_by("-forum_count")[:5]
        context["private_groups"] = ChatRoom.objects.filter(is_public=False)[
                                    :5]

        market_data = cache.get('market_data')
        if not market_data:
            market_data = fetch_and_store_market_data.delay().get()

        context.update(market_data)

        return context
