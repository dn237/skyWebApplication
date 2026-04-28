from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileAvatarForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail 

# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user_email = form.cleaned_data.get('email')
            send_mail(
                'Welcome to Sky Web!',
                f'Hi {username}, your account has been created successfully.',
                'admin@skyweb.com',
                [user_email],
                fail_silently=False,
            )
            messages.success(request, f'New user "{username}" registered successfully!')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login(request):
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Username and password do not match.')
    
    for field_name in form.fields:
        form.fields[field_name].widget.attrs.update({
            'class': 'form-control sky-input',
            'placeholder': f'Enter {form.fields[field_name].label}'
        })
    return render(request, 'accounts/login.html', {'form': form})

# This unified logout view handles the redirection safely.
def logout_view(request):
    auth_logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


def user_access(request):
    """Admin page for managing user access and permissions"""
    from django.contrib.auth import get_user_model
    from django.contrib.auth.decorators import user_passes_test
    
    # This view requires admin privileges
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    User = get_user_model()
    users = User.objects.all().order_by('username')
    
    return render(request, 'accounts/user_access.html', {
        'users': users,
    })

def profile(request):
    """User profile page showing basic information"""
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in to view your profile.')
        return redirect('accounts:login')

    from .models import UserProfile
    from teams.models import Team

    profile_obj, _ = UserProfile.objects.select_related('team', 'department').get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        avatar_form = ProfileAvatarForm(request.POST, request.FILES, instance=profile_obj)
        if avatar_form.is_valid():
            avatar_form.save()
            messages.success(request, 'Profile picture updated successfully.')
            return redirect('accounts:profile')
        messages.error(request, 'Could not update profile picture. Please use a valid image file.')
    else:
        avatar_form = ProfileAvatarForm(instance=profile_obj)

    led_teams = (
        request.user.led_teams.select_related('dept')
        .prefetch_related('members', 'projects')
        .order_by('team_name')
    )

    member_team = profile_obj.team
    show_member_team_card = bool(member_team and member_team.lead_user_id != request.user.id)

    if show_member_team_card:
        member_team = (
            Team.objects.select_related('dept', 'lead_user')
            .prefetch_related('members', 'projects')
            .get(pk=profile_obj.team.pk)
        )
    
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'profile_obj': profile_obj,
        'avatar_form': avatar_form,
        'led_teams': led_teams,
        'member_team': member_team,
        'show_member_team_card': show_member_team_card,
    })