# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================
def admin_context(request):
    """
    Context processor that adds is_admin flag to all templates.
    This allows the sidebar and other templates to check admin status globally.
    """
    return {
        'is_admin': request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
    }
# =================================================


def user_profile_context(request):
    """Provide user profile data to global templates like the sidebar."""
    if not request.user.is_authenticated:
        return {'sidebar_profile': None}

    from accounts.models import UserProfile

    profile = UserProfile.objects.filter(user=request.user).first()
    return {'sidebar_profile': profile}