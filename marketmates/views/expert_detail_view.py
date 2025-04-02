from django.views.generic import DetailView

from ..models import Expert, Forum


class ExpertDetailView(DetailView):
    """View for displaying expert profile details."""
    model = Expert
    template_name = "marketmates/expert_detail.html"
    context_object_name = "expert"

    def get_context_data(self, **kwargs):
        """Adds forums created by this expert to the context."""
        context = super().get_context_data(**kwargs)
        context["forums"] = Forum.objects.filter(created_by=self.object.user).order_by("-created_at")
        return context
