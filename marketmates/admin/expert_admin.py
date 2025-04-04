from django.contrib import admin
from django.utils import timezone
from ..models import Expert


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Expert model, allowing for
    expert verification approvals and management.
    """

    readonly_fields = ('user', 'designation', 'document', 'verified_at')
    list_display = ('user', 'designation', 'status', 'verified_at')
    list_filter = ('status', 'verified_at')
    actions = ['approve_expert']

    fieldsets = (
        ("Expert Information", {'fields': ('user', 'designation')}),
        ("Verification Details",
         {'fields': ('document', 'status', 'verified_at')}),
    )

    def has_add_permission(self, request, obj=None):
        """Prevents adding new experts manually from the admin panel."""
        return False

    def changelist_view(self, request, extra_context=None):
        """Customizes the list view title."""
        extra_context = extra_context or {}
        extra_context['title'] = 'Expert Verifications'
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Customizes the edit view title."""
        extra_context = extra_context or {}
        expert = self.get_object(request, object_id)
        extra_context['title'] = f"Expert Verification: {expert}"
        extra_context['subtitle'] = None
        return super().change_view(request, object_id, form_url,
                                   extra_context=extra_context)

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        """Hides unnecessary buttons in the admin panel."""
        context.update({
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change,
                                          form_url, obj)

    def approve_expert(self, request, queryset):
        """Approves selected experts by updating their status."""
        updated = 0
        for expert in queryset:
            if expert.status == 'Pending':
                expert.status = 'Approved'
                expert.save()
                updated += 1
        self.message_user(request, f"{updated} expert(s) approved successfully.")

    approve_expert.short_description = "Approve selected experts"
