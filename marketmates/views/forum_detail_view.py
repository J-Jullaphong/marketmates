from django.views.generic import DetailView
from ..models import Forum


class ForumDetailView(DetailView):
    model = Forum
    template_name = "marketmates/forum_detail.html"
    context_object_name = "forum"
