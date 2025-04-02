from django.views.generic import ListView

from ..models import Expert


class ExpertListView(ListView):
    """View for displaying a list of approved experts."""
    model = Expert
    template_name = "marketmates/expert_list.html"
    context_object_name = "experts"

    def get_queryset(self):
        """Returns a queryset of experts with status='Approved'."""
        return Expert.objects.filter(status="Approved")

    def get_context_data(self, **kwargs):
        """Adds top 10 ranked approved experts to the context."""
        context = super().get_context_data(**kwargs)
        context["top_experts"] = Expert.objects.filter(status="Approved").order_by("rank")[:10]
        return context
