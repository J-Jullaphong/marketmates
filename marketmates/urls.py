from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *

app_name = 'marketmates'

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("forum/<uuid:pk>/", ForumDetailView.as_view(), name="forum_detail"),
    path("create-forum/", CreateForumView.as_view(), name="create_forum"),
    path("forums/", ForumListView.as_view(), name="forum_list"),
    path("market/", MarketUpdateView.as_view(), name="market_update"),
    path("chat/", ChatRoomListView.as_view(), name="chat_room_list"),
    path("chat/<uuid:room_id>/", ChatRoomView.as_view(), name="chat_room_page"),
    path('chat/add_members/<uuid:room_id>/', add_members, name='add_member'),
    path('chat/remove_member/<uuid:room_id>/<uuid:user_id>/', remove_member, name='remove_member'),

    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("registration/", RegistrationFormView.as_view(), name="registration"),

    path("profile/", ProfileView.as_view(), name="profile"),
]
