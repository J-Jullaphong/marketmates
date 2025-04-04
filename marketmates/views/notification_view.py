from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from notifications.models import Notification


class NotificationView(LoginRequiredMixin, ListView):
    """View to display non-chat notifications for the current user."""
    model = Notification
    template_name = 'marketmates/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 10

    def get_queryset(self):
        """Returns a queryset of non-chat notifications for the current user."""
        queryset = Notification.objects.filter(
            recipient=self.request.user,
            level='info'
        ).order_by('-timestamp')
        queryset.update(unread=False)
        return queryset
