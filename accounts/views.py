from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
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