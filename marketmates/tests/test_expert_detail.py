from django.urls import reverse
from .basecase import BaseCase


class ExpertDetailViewTests(BaseCase):
    """
    Integration tests for the Expert Detail View.
    Covers functionality including status code, template rendering,
    context data, expert info display, and related forum visibility.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse("marketmates:expert_detail", args=[self.expert1.id])

    def test_expert_detail_view_returns_status_200(self):
        """Should return HTTP 200 OK when accessing expert detail."""
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_expert_detail_view_uses_correct_template(self):
        """Should use expert_detail.html template."""
        response = self.client1.get(self.url)
        self.assertTemplateUsed(response, "marketmates/expert_detail.html")

    def test_expert_detail_view_context_contains_expert(self):
        """Should include 'experts' in context."""
        response = self.client1.get(self.url)
        self.assertIn("expert", response.context)
        self.assertEqual(response.context["expert"], self.expert1)

    def test_expert_detail_view_displays_expert_info(self):
        """Should display expert's name, designation and user profile description."""
        response = self.client1.get(self.url)
        self.assertContains(response, self.expert1.user.username)
        self.assertContains(response, self.expert1.user.profile_description)
        self.assertContains(response, self.expert1.designation)

    def test_expert_detail_view_displays_forums_created_by_expert(self):
        """Should show forums created by this expert (exper1)."""
        response = self.client1.get(self.url)
        # Expert form 1 and 2 are created by expert 1
        self.assertContains(response, self.expert_forum1.title)
        self.assertContains(response, self.expert_forum2.title)
        # Expert form 1 and 2 aren't created by expert 1
        self.assertNotContains(response, self.expert_forum3.title)
        self.assertNotContains(response, self.expert_forum4.title)

    def test_expert_detail_view_returns_404_for_nonexistent_id(self):
        """Should return 404 when forum UUID does not exist."""
        url = reverse("marketmates:expert_detail", args=["00000000-0000-0000-0000-000000000000"])
        response = self.client1.get(url)
        self.assertEqual(response.status_code, 404)
