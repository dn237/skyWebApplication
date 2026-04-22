from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail 

def signup(request):
    if request.method == 'POST':
        # 1. Capture the data from the Figma form
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            # 2. Save the user to the database
            user = form.save()
            username = form.cleaned_data.get('username')
            user_email = form.cleaned_data.get('email')

            # 3. Trigger the Console Email
            send_mail(
                'Welcome to Sky Web!',
                f'Hi {username}, your account has been created successfully.',
                'admin@skyweb.com',
                [user_email],
                fail_silently=False,
            )

            # 4. Show success message and go to Login
            messages.success(request, f'New user "{username}" registered. Check your terminal for the email!')
            return redirect('accounts:login')
        else:
            # 5. Handle errors (e.g., passwords don't match)
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request: Show a blank form
        form = CustomUserCreationForm()
        
    return render(request, 'accounts/signup.html', {'form': form})

def login(request):
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        for field_name in form.fields:
            form.fields[field_name].widget.attrs.update({
                'class': 'form-control sky-input',
                'placeholder': f'Enter {form.fields[field_name].label}'
            })
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
    else:
        for field_name in form.fields:
            form.fields[field_name].widget.attrs.update({
                'class': 'form-control sky-input',
                'placeholder': f'Enter {form.fields[field_name].label}'
            })
    
    return render(request, 'accounts/login.html', {'form': form})