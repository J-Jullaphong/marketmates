import logging

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # Use the default authentication form


class LoginView(LoginView):
    template_name = 'marketmates/login.html'
    next_page = "marketmates:home"
    authentication_form = AuthenticationForm  # Changed from OTPAuthenticationForm to AuthenticationForm

    def form_valid(self, form):
        """User successful login"""
        user = form.get_user()
        messages.success(self.request, f"Login successful. Welcome {user.username}.")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle unsuccessful login attempts"""
        email = self.request.POST.get('username', '....@xxx.com')
        messages.error(self.request, "Login failed. Please check your credentials and try again.")
        context = self.get_context_data(form=form)
        context['user_email'] = email
        return self.render_to_response(context)
