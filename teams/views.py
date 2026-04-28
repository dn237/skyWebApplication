# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

"""Views for the teams app.

These pages handle the team list, team details, member rosters, project
pages, dependency pages, and the update tools used by team leads.
Where the same flow repeats, the code uses class-based views so the logic
stays in one place and is easier to follow.
"""

from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, FormView, DeleteView, TemplateView
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, Team, TeamUpdate
from .forms import TeamForm, TeamUpdateForm
from accounts.models import UserProfile

class TeamListView(ListView):
    """Show the teams list with search, filters, and sorting."""

    model = Team
    template_name = "teams/team_list.html"
    context_object_name = "teams"

    def get_queryset(self):
        queryset = Team.objects.select_related("dept", "lead_user").annotate(
            computed_count=Count("members", distinct=True),
            repo_count=Count("projects", distinct=True),
        )

        self.search_query = self.request.GET.get("q", "").strip()
        self.selected_departments = self.request.GET.getlist("departments")
        self.selected_sort = self.request.GET.get("sort", "name_asc")
        self.view_type = self.request.GET.get("view", "grid")

        if self.search_query:
            queryset = queryset.filter(
                Q(team_name__icontains=self.search_query)
                | Q(mission_statement__icontains=self.search_query)
                | Q(dept__dept_name__icontains=self.search_query)
            )

        if self.selected_departments:
            queryset = queryset.filter(dept__dept_name__in=self.selected_departments)

        if self.selected_sort == "name_desc":
            return queryset.order_by("-team_name")
        if self.selected_sort == "date_newest":
            return queryset.order_by("-team_id")
        if self.selected_sort == "date_oldest":
            return queryset.order_by("team_id")
        return queryset.order_by("team_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = (
            Team.objects.select_related("dept")
            .values_list("dept__dept_name", flat=True)
            .order_by("dept__dept_name")
            .distinct()
        )
        context["search_query"] = getattr(self, "search_query", "")
        context["selected_departments"] = getattr(self, "selected_departments", [])
        context["selected_sort"] = getattr(self, "selected_sort", "name_asc")
        context["view_type"] = getattr(self, "view_type", "grid")
        return context


class TeamDetailView(DetailView):
    """Show one team's profile page."""

    model = Team
    template_name = "teams/team_profile.html"
    pk_url_kwarg = "team_id"
    context_object_name = "team"

    def get_queryset(self):
        return Team.objects.select_related("dept", "lead_user").annotate(
            computed_member_count=Count("members", distinct=True),
            computed_repo_count=Count("projects", distinct=True),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_admin = self.request.user.is_staff or self.request.user.is_superuser  # type: ignore[attr-defined]
        is_leader = self.request.user == self.object.lead_user
        context["dependencies"] = self.object.downstream_dependencies.all()
        context["can_edit"] = is_admin or is_leader
        context["is_admin"] = is_admin
        return context


teamsHome = TeamListView.as_view()
teamsProfile = TeamDetailView.as_view()


class TeamContextMixin(ContextMixin):
    """Tiny helper for views that all start from the same team."""

    team_context_name = "team"

    def get_team(self):
        return get_object_or_404(
            Team.objects.select_related("dept", "lead_user"),
            pk=self.kwargs["team_id"],  # type: ignore[attr-defined]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.team_context_name] = self.get_team()
        return context


class TeamMembersView(TeamContextMixin, TemplateView):
    """Show the people on this team."""

    template_name = "teams/team_members.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = context["team"]
        context["members"] = UserProfile.objects.select_related("user").filter(team=team).order_by("user__username")
        return context


class TeamProjectsView(TeamContextMixin, TemplateView):
    """Show the projects linked to this team."""

    template_name = "teams/team_projects.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = context["team"].projects.all()
        return context


class TeamDependenciesView(TeamContextMixin, TemplateView):
    """Show which teams this team depends on."""

    template_name = "teams/team_dependencies.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dependencies"] = context["team"].downstream_dependencies.select_related("target_team").all()
        return context


class TeamRepositoriesView(TeamContextMixin, TemplateView):
    """Show the projects that look like code repositories."""

    template_name = "teams/team_repositories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["repositories"] = context["team"].projects.filter(description__icontains="github.com").all()
        return context


class ProjectDetailView(DetailView):
    """Show one project and make sure it belongs to the right team."""

    model = Project
    template_name = "teams/project_detail.html"
    pk_url_kwarg = "pk"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.select_related("team", "team__dept", "team__lead_user")

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs["pk"], team_id=self.kwargs["team_id"])


teamMembers = TeamMembersView.as_view()
teamProjects = TeamProjectsView.as_view()
teamDependencies = TeamDependenciesView.as_view()
teamRepositories = TeamRepositoriesView.as_view()
projectDetail = ProjectDetailView.as_view()

class TeamPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Shared permission check for the views that let people edit teams."""

    permission_mode = "lead_or_admin"

    def get_team(self):
        return get_object_or_404(
            Team.objects.select_related("dept", "lead_user"),
            pk=self.kwargs["team_id"],  # type: ignore[attr-defined]
        )

    def user_can_access(self, team):
        if self.permission_mode == "lead_only":
            return team.lead_user == self.request.user  # type: ignore[attr-defined]
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user == team.lead_user  # type: ignore[attr-defined]

    def test_func(self):
        return self.user_can_access(self.get_team())


class TeamUpdateView(TeamPermissionMixin, UpdateView):
    """Edit a team and handle the quick add/remove member actions."""

    model = Team
    form_class = TeamForm
    template_name = "teams/team_form.html"
    pk_url_kwarg = "team_id"

    def get_queryset(self):
        return Team.objects.select_related("dept", "lead_user")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Team "{self.object.team_name}" has been updated successfully.')
        return response

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_model = get_user_model()

        add_user_id = request.POST.get("add_user_id")
        remove_user_id = request.POST.get("remove_user_id")

        if add_user_id:
            user = get_object_or_404(user_model, pk=add_user_id)
            profile, _ = UserProfile.objects.get_or_create(user=user)

            if profile.team == self.object:
                messages.info(request, f"{user.username} is already in this team.")  # type: ignore[attr-defined]
            else:
                profile.team = self.object
                profile.save(update_fields=["team"])
                messages.success(request, f"{user.username} was added to {self.object.team_name}.")  # type: ignore[attr-defined]
            return redirect("teams:edit", team_id=self.object.pk)

        if remove_user_id:
            profile = get_object_or_404(UserProfile, user_id=remove_user_id, team=self.object)
            username = profile.user.username
            profile.team = None
            profile.save(update_fields=["team"])
            messages.success(request, f"{username} was removed from {self.object.team_name}.")
            return redirect("teams:edit", team_id=self.object.pk)

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_members"] = UserProfile.objects.select_related("user").filter(team=self.object).order_by("user__username")
        context["available_profiles"] = UserProfile.objects.select_related("user").exclude(team=self.object).order_by("user__username")
        context["users_without_profile"] = get_user_model().objects.filter(profile__isnull=True).order_by("username")
        return context

    def get_success_url(self):
        return reverse("teams:detail", kwargs={"team_id": self.object.pk})


class TeamUpdateCreateView(TeamPermissionMixin, FormView):
    """Let the team lead post a short update."""

    form_class = TeamUpdateForm
    template_name = "teams/add_update.html"
    permission_mode = "lead_only"

    def form_valid(self, form):
        team = self.get_team()
        update = form.save(commit=False)
        update.team = team
        update.author = self.request.user
        update.save()
        messages.success(self.request, "Update posted.")
        return redirect("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = self.get_team()
        return context


class TeamUpdateDeleteView(TeamPermissionMixin, DeleteView):
    """Delete a team update after a quick confirmation."""

    model = TeamUpdate
    template_name = "teams/delete_update.html"
    pk_url_kwarg = "update_id"
    permission_mode = "lead_only"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return TeamUpdate.objects.select_related("team", "author").filter(team_id=self.kwargs["team_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = self.object.team
        return context

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Update deleted.")
        return response


class TeamUpdateManageView(TeamUpdateCreateView):
    """Show the update form and the team's recent updates on one page."""

    template_name = "teams/manage_updates.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_team()
        context["team"] = team
        context["updates"] = team.updates.all()
        return context

    def form_valid(self, form):
        team = self.get_team()
        update = form.save(commit=False)
        update.team = team
        update.author = self.request.user
        update.save()
        messages.success(self.request, "Update posted.")
        return redirect("teams:manage_updates", team_id=team.pk)


teamsHome = TeamListView.as_view()
teamsProfile = TeamDetailView.as_view()
editTeam = TeamUpdateView.as_view()
add_team_update = TeamUpdateCreateView.as_view()
delete_team_update = TeamUpdateDeleteView.as_view()
manage_team_updates = TeamUpdateManageView.as_view()


def older_team_updates(request, team_id):
    """Return the older team updates as JSON for the dashboard's 'show more' button."""
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