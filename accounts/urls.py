from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_not_required
from . import views

# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

app_name = 'accounts'

urlpatterns = [
    path('signup/', login_not_required(views.SignupView.as_view()), name='signup'),
    path('login/', login_not_required(views.LoginView.as_view()), name='login'),
    
    # These names match the links in base.html
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user-access/', views.UserAccessView.as_view(), name='user_access'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # Password reset pages
    path('password-reset/', login_not_required(auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        success_url=reverse_lazy('accounts:password_reset_done'),
    )), name='password_reset'),
    
    path('password-reset/done/', login_not_required(auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    )), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', login_not_required(auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete'),
    )), name='password_reset_confirm'),
    
    path('reset/done/', login_not_required(auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    )), name='password_reset_complete'),

]