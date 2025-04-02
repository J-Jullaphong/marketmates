from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


from ..models import FavoriteForum


class FavoriteForumListView(LoginRequiredMixin, ListView):
    """View for displaying a list of forums favorited by the current user."""
    model = FavoriteForum
    template_name = 'marketmates/favorite_forums_list.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        """Returns the favorite forums for the current user."""
        return FavoriteForum.objects.filter(user=self.request.user).select_related('forum')
