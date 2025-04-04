from django.urls import reverse
from .basecase import BaseCase


class FavoriteForumListViewTests(BaseCase):
    """
    Integration tests for the Favorite Forum List View.

    Covers functionality including status code, authentication, template rendering,
    context data, and content display for favorited forums.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse("marketmates:favorite_forum_list")

    def test_favorite_forum_list_view_requires_login(self):
        """Should redirect if user is not authenticated."""
        self.client1.logout()
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_favorite_forum_list_view_returns_status_200_for_authenticated_user(self):
        """Should return HTTP 200 OK for authenticated user."""
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_favorite_forum_list_view_uses_correct_template(self):
        """Should use favorite_forums_list.html template."""
        response = self.client1.get(self.url)
        self.assertTemplateUsed(response, "marketmates/favorite_forums_list.html")

    def test_favorite_forum_list_view_context_contains_favorites(self):
        """Should include 'favorites' in context with favorited forum."""
        response = self.client1.get(self.url)
        self.assertIn("favorites", response.context)
        favorites = response.context["favorites"]
        self.assertEqual(len(favorites), 1)
        self.assertEqual(favorites[0].forum, self.forum1)

    def test_favorite_forum_list_view_displays_favorited_forum_info(self):
        """Should display favorited forum title, created by, and created at."""
        response = self.client1.get(self.url)
        self.assertContains(response, self.forum1.title)
        self.assertContains(response, self.forum1.created_by)
        self.assertContains(response, self.forum1.created_at.strftime("%b %d, %Y"))

    def test_favorite_forum_list_view_shows_empty_state_when_no_favorites(self):
        """Should show empty state when no favorites exist."""
        self.favorite.delete()
        response = self.client1.get(self.url)
        self.assertContains(response, "You haven’t added any favorite forums yet.")
