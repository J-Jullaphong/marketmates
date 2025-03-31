from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from marketmates.models.favorite_forum import FavoriteForum


class FavoriteForumListView(LoginRequiredMixin, ListView):
    model = FavoriteForum
    template_name = 'marketmates/favorite_forums_list.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return FavoriteForum.objects.filter(user=self.request.user).select_related('forum')
