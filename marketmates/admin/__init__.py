from django.contrib import admin

from ..models import Forum, User, Comment
from .expert_admin import ExpertAdmin
from .user_admin import UserAdmin

admin.site.register(Forum)
admin.site.register(Comment)
