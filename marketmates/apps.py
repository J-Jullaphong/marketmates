from django.apps import AppConfig


class MarketmatesConfig(AppConfig):
    """
    App configuration for the MarketMates application.
    Sets default primary key field type and application name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketmates'
