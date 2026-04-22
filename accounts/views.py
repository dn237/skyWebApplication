from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'New user "{username}" registered.')
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