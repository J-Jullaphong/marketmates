from django.views.generic import ListView
from django.db.models import Count, Q
from django.utils import timezone

from ..models import Expert, Tag


class ExpertListView(ListView):
    """View for displaying a list of approved experts."""
    model = Expert
    template_name = "marketmates/expert_list.html"
    context_object_name = "experts"

    def get_queryset(self):
        """Returns a queryset of experts with status='Approved'."""
        return Expert.objects.filter(status="Approved")

    def get_context_data(self, **kwargs):
        """Adds top 5 ranked approved experts to the context."""
        context = super().get_context_data(**kwargs)
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
        context["tags"] = Tag.objects.annotate(forum_count=Count("forum")).order_by("-forum_count")[:5]
        return context
