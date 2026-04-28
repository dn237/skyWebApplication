"""Views for the accounts app.

These cover signup, login, logout, profile editing, and the simple user
access page shown to admins.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView

# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================
from .forms import CustomUserCreationForm, ProfileAvatarForm
from .models import UserProfile
from teams.models import Team


class SignupView(FormView):
    """Create a new account and send the welcome email."""

    template_name = 'accounts/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        user_email = form.cleaned_data.get('email') or ''
        send_mail(
            'Welcome to Sky Web!',
            f'Hi {username}, your account has been created successfully.',
            'admin@skyweb.com',
            [user_email],
            fail_silently=False,
        )
        messages.success(self.request, f'New user "{username}" registered successfully!')
        return redirect('accounts:login')


class LoginView(FormView):
    """Log a user in with Django's built-in authentication form."""

    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = authenticate(
            self.request,
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password'),
        )
        if user is not None:
            auth_login(self.request, user)
            return redirect('dashboard')

        messages.error(self.request, 'Username and password do not match.')
        return self.form_invalid(form)


class LogoutView(View):
    """Log the user out and send them back to the login page."""

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('accounts:login')

    post = get


class UserAccessView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Show the user list to staff and superusers only."""

    template_name = 'accounts/user_access.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser  # type: ignore[attr-defined]

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('dashboard')

    def get_queryset(self):
        User = get_user_model()
        return User.objects.all().order_by('username')


class ProfileView(LoginRequiredMixin, FormView):
    """Show the current user's profile and let them update their avatar."""

    template_name = 'accounts/profile.html'
    form_class = ProfileAvatarForm
    success_url = reverse_lazy('accounts:profile')

    def get_profile(self):
        profile_obj, _ = UserProfile.objects.select_related('team', 'department').get_or_create(
            user=self.request.user
        )
        return profile_obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_profile()
        if self.request.method == 'POST':
            kwargs['files'] = self.request.FILES
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Profile picture updated successfully.')
        return redirect('accounts:profile')

    def form_invalid(self, form):
        messages.error(self.request, 'Could not update profile picture. Please use a valid image file.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_obj = self.get_profile()

        # Load teams the user leads so the profile page can show them.
        led_teams = (
            self.request.user.led_teams.select_related('dept')  # type: ignore[attr-defined]
            .prefetch_related('members', 'projects')
            .order_by('team_name')
        )

        member_team = profile_obj.team
        show_member_team_card = bool(member_team and member_team.lead_user_id != self.request.user.id)  # type: ignore[attr-defined]

        if show_member_team_card:
            member_team = (
                Team.objects.select_related('dept', 'lead_user')
                .prefetch_related('members', 'projects')
                .get(pk=profile_obj.team.pk)
            )

        context['user'] = self.request.user
        context['profile_obj'] = profile_obj
        context['led_teams'] = led_teams
        context['member_team'] = member_team
        context['show_member_team_card'] = show_member_team_card
        return context


signup = SignupView.as_view()
login = LoginView.as_view()
logout_view = LogoutView.as_view()
user_access = UserAccessView.as_view()
profile = ProfileView.as_view()