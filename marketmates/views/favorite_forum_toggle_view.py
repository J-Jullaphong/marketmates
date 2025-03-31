from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from marketmates.models.forum import Forum
from marketmates.models.favorite_forum import FavoriteForum


class ToggleFavoriteForumView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        forum_id = request.POST.get("forum_id")
        forum = get_object_or_404(Forum, id=forum_id)
        favorite, created = FavoriteForum.objects.get_or_create(user=request.user, forum=forum)
        if not created:
            favorite.delete()
            return JsonResponse({"favorited": False})
        return JsonResponse({"favorited": True})
