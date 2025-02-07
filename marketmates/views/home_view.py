from django.views.generic import TemplateView
from ..models import Forum, Tag, ChatRoom


class HomeView(TemplateView):
    template_name = "marketmates/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forums"] = Forum.objects.all().order_by("-created_at")[:5]
        context["tags"] = Tag.objects.all()[:6]
        context["private_groups"] = ChatRoom.objects.filter(is_public=False)[:5]
        return context
