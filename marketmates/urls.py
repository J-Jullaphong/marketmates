from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

app_name = 'marketmates'

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("forum/<uuid:pk>/", ForumDetailView.as_view(), name="forum_detail"),
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("registration/", RegistrationFormView.as_view(), name="registration")
]
