from django.contrib import admin

from ..models import Forum

from .expert_admin import ExpertAdmin

admin.site.register(Forum)
