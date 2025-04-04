from django.urls import reverse
from .basecase import BaseCase
from django.utils.timesince import timesince


class ForumDetailViewTests(BaseCase):
    """
    Integration tests for the Forum Detail view.
    Covers functionality including status code, template rendering,
    context data and comments section.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse("marketmates:forum_detail", args=[self.forum1.id])

    def test_forum_detail_view_returns_status_200(self):
        """Should return HTTP 200 OK when accessing forum detail."""
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_forum_detail_view_uses_correct_template(self):
        """Should use forum_detail.html template."""
        response = self.client1.get(self.url)
        self.assertTemplateUsed(response, "marketmates/forum_detail.html")

    def test_forum_detail_view_context_contains_forum(self):
        """Should include 'forum' in context."""
        response = self.client1.get(self.url)
        self.assertEqual(response.context["forum"], self.forum1)

    def test_forum_detail_view_displays_forum_title_and_description(self):
        """Should display title, description, created by and created at."""
        response = self.client1.get(self.url)
        self.assertContains(response, self.forum1.title)
        self.assertContains(response, self.forum1.description)
        self.assertContains(response, self.forum1.created_by)
        self.assertContains(response, timesince(self.forum1.created_at) + " ago")

    def test_forum_detail_view_displays_existing_comments(self):
        """Should display all existing comments."""
        response = self.client1.get(self.url)
        self.assertContains(response, self.comment1.comment_content)
        self.assertContains(response, self.comment1.user.username)
        self.assertNotContains(response, self.comment2.comment_content)

    def test_forum_detail_view_shows_comment_form_when_authenticated(self):
        """Should show form when user is logged in."""
        response = self.client1.get(self.url)
        self.assertContains(response, "Leave a Response")
        self.assertContains(response, "<form", html=False)

    def test_forum_detail_view_hides_comment_form_when_anonymous(self):
        """Should hide form when user is logged out."""
        self.client1.logout()
        response = self.client.get(self.url)
        self.assertNotContains(response, "Leave a Response")
        self.assertContains(response, "You must be logged in to leave a response")

    def test_forum_detail_view_with_nonexistent_forum_returns_404(self):
        """Should return 404 when forum UUID does not exist."""
        url = reverse("marketmates:forum_detail", args=["00000000-0000-0000-0000-000000000000"])
        response = self.client1.get(url)
        self.assertEqual(response.status_code, 404)
