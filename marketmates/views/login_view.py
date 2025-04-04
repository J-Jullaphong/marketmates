import logging

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

db_logger = logging.getLogger('db')


class LoginView(LoginView):
    """View for handling user login using Django's built-in authentication form."""
    template_name = 'marketmates/login.html'
    next_page = "marketmates:home"
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        """User successful login"""
        user = form.get_user()
        messages.success(self.request, f"Login successful. Welcome {user.username}.")
        db_logger.info(f"User '{user.username}' logged in successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle unsuccessful login attempts"""
        email = self.request.POST.get('username', '....@xxx.com')
        db_logger.warning(f"Failed login attempt for emai: {email}")
        context = self.get_context_data(form=form)
        context['user_email'] = email
        return self.render_to_response(context)
