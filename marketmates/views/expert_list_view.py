from django.views.generic import ListView
from ..models import Expert


class ExpertListView(ListView):
    model = Expert
    template_name = "marketmates/expert_list.html"
    context_object_name = "experts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_experts"] = Expert.objects.order_by("rank")[:10]
        return context
