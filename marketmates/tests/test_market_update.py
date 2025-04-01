from django.urls import reverse
from unittest.mock import patch
from django.core.cache import cache
from .basecase import BaseCase


class MarketUpdateViewTests(BaseCase):
    """
    Integration tests for the Market Update View.
    Covers functionality including status code, template rendering,
    context data and fallback behavior.
    """

    def setUp(self):
        super().setUp()
        self.url = reverse("marketmates:market_update")
        cache.clear()

    @patch("marketmates.views.market_update_view.fetch_and_store_market_data.delay")
    def test_market_update_view_returns_status_200(self, mock_task):
        """Should return 200 OK when accessing the view."""
        mock_task.return_value.get.return_value = {"stock_data": []}
        response = self.client1.get(self.url)
        self.assertEqual(response.status_code, 200)

    @patch("marketmates.views.market_update_view.fetch_and_store_market_data.delay")
    def test_market_update_view_uses_correct_template(self, mock_task):
        """Should render using the correct template."""
        mock_task.return_value.get.return_value = {"stock_data": []}
        response = self.client1.get(self.url)
        self.assertTemplateUsed(response, "marketmates/market_update.html")

    @patch("marketmates.views.market_update_view.fetch_and_store_market_data.delay")
    def test_market_update_view_loads_data_from_task_when_cache_is_empty(self, mock_task):
        """Should fallback to task when cache is empty."""
        mock_task.return_value.get.return_value = {
            "stock_data": [{"symbol": "SET", "price": 1600}]
        }

        response = self.client1.get(self.url)
        self.assertIn("stock_data", response.context)
        self.assertEqual(response.context["stock_data"][0]["symbol"], "SET")
        mock_task.assert_called_once()

    @patch("marketmates.views.market_update_view.fetch_and_store_market_data.delay")
    def test_market_update_view_uses_data_from_cache_if_exists(self, mock_task):
        """Should use cached data instead of calling task."""
        cached_data = {
            "stock_data": [{"symbol": "SET", "price": 1700}]
        }
        cache.set("market_data", cached_data)

        response = self.client1.get(self.url)
        self.assertEqual(response.context["stock_data"][0]["price"], 1700)
        mock_task.assert_not_called()
