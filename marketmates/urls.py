from django.urls import path
from .views import *

app_name = 'marketmates'

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("forum/<uuid:pk>/", ForumDetailView.as_view(), name="forum_detail"),
]
