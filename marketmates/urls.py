from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *

app_name = 'marketmates'

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("forum/<uuid:pk>/", ForumDetailView.as_view(), name="forum_detail"),
    path("create-forum/", CreateForumView.as_view(), name="create_forum"),
    path("search-forums/", SearchForumView.as_view(), name="search_forums"),
    path("market/", MarketUpdateView.as_view(), name="market_update"),

    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("registration/", RegistrationFormView.as_view(), name="registration"),

    path("profile/", ProfileView.as_view(), name="profile"),
]
