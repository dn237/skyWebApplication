# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from organizations.models import Department
from .models import Team
from .models import TeamUpdate
from accounts.models import UserProfile


class TeamsViewTests(TestCase):
	"""Tests for the teams pages and update flows."""

	def setUp(self):
		User = get_user_model()
		# Create the people we use across the tests.
		self.lead = User.objects.create_user(username='leaduser', password='pass') # type: ignore
		self.member = User.objects.create_user(username='member', password='pass') # type: ignore
		self.outsider = User.objects.create_user(username='outsider', password='pass') # type: ignore
		self.department = Department.objects.create(dept_name='Engineering')

		# Build the main team and a second team for comparison.
		self.team = Team.objects.create(team_name='API Team', dept=self.department, lead_user=self.lead, focus_areas='APIs', skills_technologies='Django')
		self.other_team = Team.objects.create(team_name='Platform Team')

		# Profiles are how the UI knows who belongs where.
		UserProfile.objects.update_or_create(user=self.lead, defaults={'team': self.team, 'job_title': 'Team Lead'})
		UserProfile.objects.update_or_create(user=self.member, defaults={'team': self.team, 'job_title': 'Engineer'})
		UserProfile.objects.update_or_create(user=self.outsider, defaults={'team': self.other_team, 'job_title': 'Analyst'})

	def test_team_list_shows_team(self):
		"""The team index should render and include the created team."""
		url = reverse('teams:index')
		self.client.login(username='leaduser', password='pass')
		resp = self.client.get(url, follow=True)
		self.assertEqual(resp.status_code, 200)
		self.assertIn('API Team', resp.content.decode())

	def test_team_detail_shows_edit_controls_for_lead(self):
		"""The CBV detail page should expose edit actions to the team lead."""
		url = reverse('teams:detail', kwargs={'team_id': self.team.pk})
		self.client.login(username='leaduser', password='pass')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		body = resp.content.decode()
		self.assertIn('API Team', body)
		self.assertIn('can_edit', resp.context)

	def test_non_lead_cannot_open_team_edit_page(self):
		"""Only the lead or an admin should be allowed to open the edit page."""
		url = reverse('teams:edit', kwargs={'team_id': self.team.pk})
		self.client.login(username='outsider', password='pass')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 403)
		self.assertFalse(Team.objects.filter(pk=self.team.pk, team_name='Blocked Rename').exists())

	def test_team_lead_can_update_team_name(self):
		"""The update CBV should save team metadata changes."""
		url = reverse('teams:edit', kwargs={'team_id': self.team.pk})
		self.client.login(username='leaduser', password='pass')
		resp = self.client.post(url, {
			'team_name': 'API Team Updated',
			'focus_areas': 'Platform APIs',
			'skills_technologies': 'Django, PostgreSQL',
			'status': 'Active',
			'dept': self.department.pk,
			'lead_user': self.lead.pk,
		}, follow=True)
		self.assertEqual(resp.status_code, 200)
		self.team.refresh_from_db()
		self.assertEqual(self.team.team_name, 'API Team Updated')

	def test_team_lead_can_add_and_remove_member_through_edit_page(self):
		"""The edit CBV should still support add/remove member quick actions."""
		url = reverse('teams:edit', kwargs={'team_id': self.team.pk})
		self.client.login(username='leaduser', password='pass')

		resp_add = self.client.post(url, {'add_user_id': self.outsider.pk}, follow=True)
		self.assertEqual(resp_add.status_code, 200)
		self.outsider.profile.refresh_from_db()
		self.assertEqual(self.outsider.profile.team, self.team)

		resp_remove = self.client.post(url, {'remove_user_id': self.outsider.pk}, follow=True)
		self.assertEqual(resp_remove.status_code, 200)
		self.outsider.profile.refresh_from_db()
		self.assertIsNone(self.outsider.profile.team)

	def test_search_filters_results(self):
		"""Search parameter should filter teams and return the matching team."""
		url = reverse('teams:index')
		self.client.login(username='leaduser', password='pass')
		resp = self.client.get(url, {'q': 'API'}, follow=True)
		self.assertEqual(resp.status_code, 200)
		self.assertIn('API Team', resp.content.decode())

	def test_team_members_page_shows_members(self):
		"""Team members page should list members for the given team."""
		url = reverse('teams:members', kwargs={'team_id': self.team.pk})
		# Log in as the member so the page has a real user.
		self.client.login(username='member', password='pass')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		body = resp.content.decode()
		# The page should show either the username or the title.
		self.assertTrue('member' in body or 'Engineer' in body)

	def test_dashboard_team_section_includes_current_user(self):
		"""The dashboard roster should include the logged-in user as well."""
		url = reverse('dashboard')
		self.client.login(username='leaduser', password='pass')
		resp = self.client.get(url, follow=True)
		self.assertEqual(resp.status_code, 200)
		body = resp.content.decode()
		self.assertIn('(You)', body)
		self.assertIn('leaduser', body)
		self.assertIn('member', body)
		self.assertIn('data-roster-name="leaduser"', body)
		self.assertIn('data-roster-name="member"', body)
		self.assertLess(body.index('data-roster-name="leaduser"'), body.index('data-roster-name="member"'))
		self.assertIn('data-current-user="true"', body)

	def test_team_lead_can_add_and_delete_update(self):
		"""Team lead should be able to post and remove updates for their team."""
		url_add = reverse('teams:add_update', kwargs={'team_id': self.team.pk})
		self.client.login(username='leaduser', password='pass')
		resp = self.client.post(url_add, {'title': 'Roadmap', 'body': 'We shipped v1'}, follow=True)
		self.assertEqual(resp.status_code, 200)
		# Make sure the update shows up on the dashboard.
		dash = reverse('dashboard')
		resp2 = self.client.get(dash)
		self.assertIn('Roadmap', resp2.content.decode())

		# Pull the new update back out of the database.
		update = TeamUpdate.objects.filter(team=self.team, title='Roadmap').first()
		self.assertIsNotNone(update)

		# Delete it through the same flow a user would use.
		url_del = reverse('teams:delete_update', kwargs={'team_id': self.team.pk, 'update_id': update.pk}) # type: ignore
		resp3 = self.client.post(url_del, follow=True)
		self.assertEqual(resp3.status_code, 200)
		# Confirm the row is gone.
		self.assertFalse(TeamUpdate.objects.filter(pk=update.pk).exists()) # type: ignore

	def test_manage_updates_page_posts_update(self):
		"""The management CBV should create updates and list them on the same page."""
		url = reverse('teams:manage_updates', kwargs={'team_id': self.team.pk})
		self.client.login(username='leaduser', password='pass')
		resp = self.client.post(url, {'title': 'Sprint', 'body': 'Planning complete'}, follow=True)
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(TeamUpdate.objects.filter(team=self.team, title='Sprint').exists())
		self.assertIn('Sprint', resp.content.decode())

	def test_non_lead_cannot_manage_team_updates(self):
		"""Only the team lead should be able to use the update management page."""
		url = reverse('teams:manage_updates', kwargs={'team_id': self.team.pk})
		self.client.login(username='member', password='pass')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 403)
		self.assertFalse(TeamUpdate.objects.filter(team=self.team, title='Blocked').exists())

	def test_older_updates_endpoint_returns_updates_after_first_two(self):
		"""AJAX endpoint should return only updates older than the first two."""
		self.client.login(username='leaduser', password='pass')
		TeamUpdate.objects.create(team=self.team, author=self.lead, title='U1', body='First')
		TeamUpdate.objects.create(team=self.team, author=self.lead, title='U2', body='Second')
		TeamUpdate.objects.create(team=self.team, author=self.lead, title='U3', body='Third')
		TeamUpdate.objects.create(team=self.team, author=self.lead, title='U4', body='Fourth')

		url = reverse('teams:older_updates', kwargs={'team_id': self.team.pk})
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertIn('updates', data)
		# The endpoint excludes the 2 most recent updates
		self.assertEqual(len(data['updates']), 2)

