from django.urls import reverse
from .basecase import BaseCase


class ForumListViewTests(BaseCase):
    """
    Integration tests for the ForumListView.
    Covers functionality including status code, template rendering,
    context data, search, and sorting features.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse("marketmates:forum_list")

    # Basic View Tests
    def test_forum_list_view_returns_status_200(self):
        """Should return HTTP 200 OK."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_forum_list_view_uses_correct_template(self):
        """Should use forum_list.html template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "marketmates/forum_list.html")

    def test_forum_list_view_context_contains_forum_queryset(self):
        """Should include 'forums' in context with at least one item."""
        response = self.client.get(self.url)
        self.assertIn("forums", response.context)
        self.assertGreaterEqual(len(response.context["forums"]), 1)

    # Search Tests
    def test_search_with_full_title_returns_exact_match(self):
        """Should return only the exact forum matching full title."""
        response = self.client.get(self.url, {"q": "forum-1"})
        self.assertContains(response, "forum-1")
        self.assertNotContains(response, "forum-2")
        self.assertNotContains(response, "forum-3")

    def test_search_with_partial_title_returns_multiple_matches(self):
        """Should return all forums containing the partial title."""
        response = self.client.get(self.url, {"q": "forum"})
        self.assertContains(response, "forum-1")
        self.assertContains(response, "forum-2")
        self.assertContains(response, "forum-3")

    def test_search_with_nonexistent_title_returns_no_results(self):
        """Should return no forums when title does not match anything."""
        response = self.client.get(self.url, {"q": "nonexistent-title"})
        self.assertNotContains(response, "forum-1")
        self.assertNotContains(response, "forum-2")
        self.assertNotContains(response, "forum-3")
        self.assertContains(response, "No forums found")

    def test_search_with_special_characters_returns_no_results(self):
        """Should not crash or match anything for special character queries."""
        response = self.client.get(self.url, {"q": "#$%&*@!"})
        self.assertContains(response, "No forums found")

    def test_search_with_whitespace_returns_trimmed_results(self):
        """Should handle extra spaces in search queries gracefully."""
        response = self.client.get(self.url, {"q": "  forum-1  "})
        self.assertContains(response, "forum-1")

    def test_search_is_case_insensitive(self):
        """Should return results regardless of keyword case."""
        response = self.client.get(self.url, {"q": "FoRuM-1"})
        self.assertContains(response, "forum-1")

    # Tag Search Tests
    def test_search_by_existing_tag_returns_matching_forums(self):
        """Should return forums that have the given #tag."""
        response = self.client.get(self.url, {"q": "#tag-1"})
        self.assertContains(response, "forum-1")
        self.assertContains(response, "forum-2")
        self.assertNotContains(response, "forum-3")

    def test_search_by_nonexistent_tag_returns_no_results(self):
        """Should return no results if the tag doesn't exist."""
        response = self.client.get(self.url, {"q": "#notatag"})
        self.assertNotContains(response, "forum-1")
        self.assertNotContains(response, "forum-2")
        self.assertNotContains(response, "forum-3")
        self.assertContains(response, "No forums found")

    # Sorting Tests
    def test_sorting_by_oldest_places_oldest_forum_first(self):
        """Should place the oldest forum first when sorting by created_at."""
        response = self.client.get(self.url, {"sort": "created_at"})
        forums = list(response.context["forums"])
        self.assertEqual(forums[0], self.forum1)

    def test_sorting_by_newest_places_newest_forum_first(self):
        """Should place the newest forum first by default."""
        response = self.client.get(self.url)
        forums = list(response.context["forums"])
        self.assertEqual(forums[0], self.forum3)

