from django.core.cache import cache
from django.views.generic import TemplateView

from ..tasks import fetch_and_store_market_data


class MarketUpdateView(TemplateView):
    """View for displaying market data updates."""
    template_name = 'marketmates/market_update.html'

    def get_context_data(self, **kwargs):
        """Fetch market data for the context."""
        context = super().get_context_data(**kwargs)

        market_data = cache.get('market_data')

        if not market_data:
            market_data = fetch_and_store_market_data.delay().get()

        context.update(market_data)
        return context
