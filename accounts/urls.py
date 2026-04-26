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
    path('signup/', login_not_required(views.signup), name='signup'),
    path('login/', login_not_required(views.login), name='login'),
    
    # The crucial naming to match base.html sidebar links
    path('logout/', views.logout_view, name='logout'),
    path('user-access/', views.user_access, name='user_access'),
    path('profile/', views.profile, name='profile'),
    
    # Password Reset URLs (Integrated from main branch)
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