from django.views.generic import DetailView

from ..models import Expert, Forum, FavoriteForum


class ExpertDetailView(DetailView):
    """View for displaying expert profile details."""
    model = Expert
    template_name = "marketmates/expert_detail.html"
    context_object_name = "expert"

    def get_context_data(self, **kwargs):
        """Adds forums created by this expert to the context."""
        context = super().get_context_data(**kwargs)

        forums = Forum.objects.filter(created_by=self.object.user).order_by(
            "-created_at")
        context["forums"] = forums

        if self.request.user.is_authenticated:
            favorite_ids = FavoriteForum.objects.filter(
                user=self.request.user, forum__in=forums
            ).values_list("forum_id", flat=True)
            context["favorite_forum_ids"] = list(favorite_ids)
        else:
            context["favorite_forum_ids"] = []
        return context
