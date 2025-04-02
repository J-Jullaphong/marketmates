from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Forum, FavoriteForum


class ToggleFavoriteForumView(LoginRequiredMixin, View):
    """View for toggling a forum as favorite or removing it from favorites."""

    def post(self, request, *args, **kwargs):
        """Handles POST request to toggle favorite status of a forum."""
        forum_id = request.POST.get("forum_id")
        forum = get_object_or_404(Forum, id=forum_id)
        favorite, created = FavoriteForum.objects.get_or_create(user=request.user, forum=forum)
        if not created:
            favorite.delete()
            return JsonResponse({"favorited": False})
        return JsonResponse({"favorited": True})
