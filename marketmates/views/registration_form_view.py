from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import TemplateView

from ..forms import UserRegistrationForm, ExpertRegistrationForm


class RegistrationFormView(TemplateView):
    """View for handling the registration process for both users and experts."""
    template_name = 'marketmates/registration.html'

    def get_context_data(self, **kwargs):
        """Adds the appropriate registration form to the context based on the query parameter."""
        context = super().get_context_data(**kwargs)

        if 'form' not in context:
            form_type = self.request.GET.get('form', 'member')
            if form_type == 'verified_expert':
                context['form'] = ExpertRegistrationForm()
            else:
                context['form'] = UserRegistrationForm()

        return context

    def post(self, request, *args, **kwargs):
        """Handles POST requests for form submissions."""
        form_type = self.request.GET.get('form', 'member')

        if form_type == 'verified_expert':
            form = ExpertRegistrationForm(request.POST, request.FILES)
        else:
            form = UserRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            if form_type == 'verified_expert':
                messages.success(self.request, "Registration successful. Your account will be activated once approved.")
            else:
                login(request, user)
                messages.success(request, "Registration successful. Welcome!")
                return redirect('marketmates:home')

        messages.error(self.request, "There was an error with your submission.")
        return self.render_to_response(self.get_context_data(form=form))
