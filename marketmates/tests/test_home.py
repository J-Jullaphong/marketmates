from django.urls import reverse
from .basecase import BaseCase


class HomeViewTests(BaseCase):
    """
    Integration tests for the Home view.
    Covers functionality including status code, template rendering,
    context data, forum order display, and popular tag visibility.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse("marketmates:home")

    def test_home_view_returns_status_200(self):
        """Should return HTTP 200 OK when accessing home."""
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """Should use home.html template."""
        response = self.client1.get(self.url)
        self.assertTemplateUsed(response, "marketmates/home.html")

    def test_forum_list_view_context_contains_forum_queryset(self):
        """Should include 'forums' in context with at least one item."""
        response = self.client1.get(self.url)
        self.assertIn("forums", response.context)
        self.assertGreaterEqual(len(response.context["forums"]), 1)

    def test_home_view_displays_recent_forums_in_descending_order(self):
        """Should display forum titles from newest to oldest."""
        response = self.client1.get(self.url)
        content = response.content.decode()
        self.assertTrue(content.index(self.forum4.title) < content.index(self.forum3.title)
                        < content.index(self.forum2.title) < content.index(self.forum1.title))

    def test_home_view_displays_popular_tags_correctly(self):
        """Should display popular tags #tag-1, #tag-2, and #tag-3."""
        response = self.client1.get(self.url)
        self.assertContains(response, self.tag1.tag_name)
        self.assertContains(response, self.tag2.tag_name)
        self.assertContains(response, self.tag3.tag_name)
