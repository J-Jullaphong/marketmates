import logging

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ..models import User
from ..forms import ProfileForm

db_logger = logging.getLogger('db')


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    """View to manage user profile updates."""
    template_name = 'marketmates/profile.html'

    def get(self, request):
        """Handles the GET request to display the user profile form."""
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("marketmates:home")

        form = ProfileForm(instance=user)
        context = {
            'form': form,
            'user': user,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Handles the POST request to update user profile information."""
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("marketmates:home")

        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            db_logger.info(f"Profile updated successfully for user: {user.username} ({user.email})")
            return redirect("marketmates:profile")

        messages.error(request, "There was an error updating your profile. Please check the form and try again.")
        db_logger.warning(f"Profile update failed for user: {user.username}. Errors: {form.errors.as_json()}")
        context = {
            'form': form,
            'user': user,
        }
        return render(request, self.template_name, context)
