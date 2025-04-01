from django.urls import reverse
from .basecase import BaseCase


class NotificationViewTests(BaseCase):
    """
    Integration tests for the Notification View.
    Covers status code, template usage, context data, and behavior of notification listing.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse("marketmates:notification_list")

    def test_notification_view_requires_login(self):
        """Should redirect if user is not authenticated."""
        self.client1.logout()
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_notification_view_returns_status_200(self):
        """Should return HTTP 200 OK."""
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_notification_view_uses_correct_template(self):
        """Should use notification_list.html template for rendering."""
        response = self.client1.get(self.url)
        self.assertTemplateUsed(response, "marketmates/notification_list.html")

    def test_notification_view_context_contains_notifications(self):
        """Context should include a list of non-chat notifications."""
        response = self.client1.get(self.url)
        self.assertIn("notifications", response.context)
        notifications = response.context["notifications"]
        self.assertEqual(len(notifications), 2)
        self.assertEqual(notifications[0], self.notification2)
        self.assertEqual(notifications[1], self.notification1)

    def test_notification_view_displays_notification_verbs(self):
        """Should display notification messages/verbs in response."""
        response = self.client1.get(self.url)
        self.assertContains(response, "replied to your forum")
        self.assertContains(response, "mentioned you in a comment")

    def test_notification_view_marks_notifications_as_read(self):
        """Should mark fetched notifications as read (unread=False)."""
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.unread)

        self.client1.get(self.url)

        self.notification1.refresh_from_db()
        self.notification2.refresh_from_db()
        self.assertFalse(self.notification1.unread)
        self.assertFalse(self.notification2.unread)
