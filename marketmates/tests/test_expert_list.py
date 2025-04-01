from django.urls import reverse
from .basecase import BaseCase


class ExpertListViewTests(BaseCase):
    """
    Integration tests for the Expert List View.
    Covers functionality including status code, template rendering,
    context data, and top expert ordering
    """

    def setUp(self):
        super().setUp()
        self.url = reverse("marketmates:expert_list")

    def test_expert_list_view_returns_status_200(self):
        """Should return HTTP 200 OK when accessing expert list."""
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_expert_list_view_uses_correct_template(self):
        """Should use expert_list.html template."""
        response = self.client1.get(self.url)
        self.assertTemplateUsed(response, "marketmates/expert_list.html")

    def test_expert_list_view_context_contains_experts(self):
        """Should include 'experts' and 'top_experts' in context."""
        response = self.client1.get(self.url)
        self.assertIn("experts", response.context)
        self.assertIn("top_experts", response.context)

    def test_expert_list_view_displays_expert_names_and_designation(self):
        """Should display expert names, profile description and designation in response."""
        response = self.client1.get(self.url)
        self.assertContains(response, self.expert1.user.username)
        self.assertContains(response, self.expert1.user.profile_description)
        self.assertContains(response, self.expert1.designation)

        self.assertContains(response, self.expert2.user.username)
        self.assertContains(response, self.expert2.user.profile_description)
        self.assertContains(response, self.expert2.designation)

    def test_expert_list_view_only_shows_approved_experts(self):
        """Should show only experts with status='Approved'."""
        self.expert2.status = "Rejected"
        self.expert2.save()
        response = self.client1.get(self.url)
        self.assertContains(response, self.expert1.user.username)
        self.assertNotContains(response, self.expert2.user.username)

    def test_expert_list_view_displays_top_experts_by_rank(self):
        """Top experts should be ordered by rank (lowest = highest priority)."""
        response = self.client1.get(self.url)
        top_experts = list(response.context["top_experts"])
        self.assertEqual(top_experts[0], self.expert1)
        self.assertEqual(top_experts[1], self.expert2)

    def test_expert_list_view_returns_empty_list_when_no_approved_expert(self):
        """Should show empty state when no approved experts exist."""
        self.expert1.status = "Pending"
        self.expert2.status = "Rejected"
        self.expert1.save()
        self.expert2.save()
        response = self.client1.get(self.url)
        experts = list(response.context["experts"])
        self.assertEqual(len(experts), 0)
        self.assertContains(response, "No experts available")
