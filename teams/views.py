# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import Project, Team
from .forms import TeamForm
from accounts.models import UserProfile
from .models import TeamUpdate
from .forms import TeamUpdateForm




def teamsHome(request):
    # 1. Capture View Preference (Grid vs List)
    view_type = request.GET.get("view", "grid") 

    # 2. Existing Search/Filter/Sort Logic
    search_query = request.GET.get("q", "").strip()
    selected_departments = request.GET.getlist("departments")
    selected_sort = request.GET.get("sort", "name_asc")

    teams = Team.objects.select_related("dept", "lead_user").annotate(
        # name must match what used in HTML
        computed_count=Count("members", distinct=True), 
        repo_count=Count("projects", distinct=True) 
    )

    if search_query:
        teams = teams.filter(
            Q(team_name__icontains=search_query)
            | Q(mission_statement__icontains=search_query)
            | Q(dept__dept_name__icontains=search_query)
        )

    if selected_departments:
        teams = teams.filter(dept__dept_name__in=selected_departments)

    # Sorting logic
    if selected_sort == "name_desc":
        teams = teams.order_by("-team_name")
    elif selected_sort == "date_newest":
        teams = teams.order_by("-team_id")
    elif selected_sort == "date_oldest":
        teams = teams.order_by("team_id")
    else:
        teams = teams.order_by("team_name")

    # Get unique departments for the filter dropdown
    departments = (
        Team.objects.select_related("dept")
        .values_list("dept__dept_name", flat=True)
        .order_by("dept__dept_name")
        .distinct()
    )


    # 3. Add 'view_type' to the Context
    return render(request, "teams/team_list.html", {
        "teams": teams,
        "departments": departments,
        "search_query": search_query,
        "selected_departments": selected_departments,
        "selected_sort": selected_sort,
        "view_type": view_type, # <--- Tells HTML which layout to use
    })


def teamsProfile(request, team_id):
    # 1. Fetch team with optimized counts for the dashboard cards
    team = get_object_or_404(
        Team.objects.select_related("dept", "lead_user").annotate(
            computed_member_count=Count("members", distinct=True),
            computed_repo_count=Count("projects", distinct=True)
        ), 
        pk=team_id
    )

    # 2. Get dependencies for the sidebar
    dependencies = team.downstream_dependencies.all()

    # --- ROLE-BASED ACCESS CONTROL ---

    # 1. Admin: Has global rights (is_staff)
    is_admin = request.user.is_staff or request.user.is_superuser

    # 2. Team Leader: Has rights for THIS team specifically
    is_leader = (request.user == team.lead_user)
    
    # 3. Permission: Can they see the 'Edit' buttons?
    can_edit = is_admin or is_leader

    return render(request, 'teams/team_profile.html', {
        'team': team,
        'dependencies': team.downstream_dependencies.all(),
        'can_edit': can_edit, 
        'is_admin': is_admin,
    })

def teamMembers(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    members = UserProfile.objects.select_related('user').filter(team=team).order_by('user__username')
    
    return render(request, 'teams/team_members.html', {
        'team': team,
        'members': members
    })

def teamProjects(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    projects = team.projects.all()
    
    return render(request, 'teams/team_projects.html', {
        'team': team,
        'projects': projects
    })

def teamDependencies(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    dependencies = team.downstream_dependencies.select_related('target_team').all()
    
    return render(request, 'teams/team_dependencies.html', {
        'team': team,
        'dependencies': dependencies
    })

def teamRepositories(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    repositories = team.projects.filter(description__icontains="github.com").all()

    return render(request, 'teams/team_repositories.html', {
        'team': team,
        'repositories': repositories
    })

def projectDetail(request, team_pk, pk):
    project = get_object_or_404(Project, pk=pk, team_id=team_pk)
    return render(request, 'teams/project_detail.html', {
        'project': project
    })

@login_required
def editTeam(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    # Role-based access control
    is_admin = request.user.is_staff or request.user.is_superuser
    is_leader = request.user == team.lead_user

    if not (is_admin or is_leader):
        messages.error(request, 'You do not have permission to edit this team.')
        return redirect('teams:detail', team_id=team_id)

    User = get_user_model()

    if request.method == 'POST':
        add_user_id = request.POST.get('add_user_id')
        remove_user_id = request.POST.get('remove_user_id')

        if add_user_id:
            user = get_object_or_404(User, pk=add_user_id)
            profile, _ = UserProfile.objects.get_or_create(user=user)

            if profile.team == team:
                messages.info(request, f'{user.username} is already in this team.') # type: ignore
            else:
                profile.team = team
                profile.save(update_fields=['team'])
                messages.success(request, f'{user.username} was added to {team.team_name}.') # type: ignore

            return redirect('teams:edit', team_id=team_id)

        if remove_user_id:
            profile = get_object_or_404(UserProfile, user_id=remove_user_id, team=team)
            username = profile.user.username
            profile.team = None
            profile.save(update_fields=['team'])
            messages.success(request, f'{username} was removed from {team.team_name}.')
            return redirect('teams:edit', team_id=team_id)

        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, f'Team "{team.team_name}" has been updated successfully.')
            return redirect('teams:detail', team_id=team_id)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = TeamForm(instance=team)

    current_members = UserProfile.objects.select_related('user').filter(team=team).order_by('user__username')
    available_profiles = UserProfile.objects.select_related('user').exclude(team=team).order_by('user__username')
    users_without_profile = User.objects.filter(profile__isnull=True).order_by('username')

    return render(request, 'teams/team_form.html', {
        'form': form,
        'team': team,
        'current_members': current_members,
        'available_profiles': available_profiles,
        'users_without_profile': users_without_profile,
    })


@login_required
def add_team_update(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    # only the lead can create updates
    if team.lead_user != request.user:
        messages.error(request, 'Only the team lead can post updates.')
        return redirect('teams:detail', team_id=team_id)

    if request.method == 'POST':
        form = TeamUpdateForm(request.POST)
        if form.is_valid():
            upd = form.save(commit=False)
            upd.team = team
            upd.author = request.user
            upd.save()
            messages.success(request, 'Update posted.')
            return redirect('dashboard')
    else:
        form = TeamUpdateForm()

    return render(request, 'teams/add_update.html', {'form': form, 'team': team})


@login_required
def delete_team_update(request, team_id, update_id):
    team = get_object_or_404(Team, pk=team_id)
    update = get_object_or_404(TeamUpdate, pk=update_id, team=team)

    if team.lead_user != request.user:
        messages.error(request, 'Only the team lead can delete updates.')
        return redirect('teams:detail', team_id=team_id)

    if request.method == 'POST':
        update.delete()
        messages.success(request, 'Update deleted.')
        return redirect('dashboard')

    return render(request, 'teams/delete_update.html', {'update': update, 'team': team})

@login_required
def manage_team_updates(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if team.lead_user != request.user:
        messages.error(request, 'Only the team lead may manage updates.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = TeamUpdateForm(request.POST)
        if form.is_valid():
            upd = form.save(commit=False)
            upd.team = team
            upd.author = request.user
            upd.save()
            messages.success(request, 'Update posted.')
            return redirect('teams:manage_updates', team_id=team.pk)
    else:
        form = TeamUpdateForm()

    updates = team.updates.all()

    return render(request, 'teams/manage_updates.html', {
        'team': team,
        'form': form,
        'updates': updates
    })

@login_required
def older_team_updates(request, team_id):
    """Return older team updates (everything after the first 2) as JSON.

    Used by the dashboard "Show more" control to lazy-load older items.
    Access is limited to team members, team lead, or admins.
    """
    team = get_object_or_404(Team, pk=team_id)
    profile = UserProfile.objects.filter(user=request.user).first()

    is_member = bool(profile and profile.team == team)
    is_lead = team.lead_user == request.user
    is_admin = request.user.is_staff or request.user.is_superuser

    if not (is_member or is_lead or is_admin):
        return JsonResponse({'detail': 'Forbidden'}, status=403)

    updates = TeamUpdate.objects.filter(team=team)[2:]
    payload = {
        'updates': [
            {
                'id': upd.pk,
                'title': upd.title,
                'body': upd.body,
                'author': upd.author.get_full_name() if upd.author and upd.author.get_full_name() else (upd.author.username if upd.author else 'Unknown'),
                'created_at': upd.created_at.strftime('%b %d'),
            }
            for upd in updates
        ]
    }
    return JsonResponse(payload)