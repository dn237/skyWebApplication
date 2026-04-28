# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Team
from .models import TeamUpdate
from accounts.models import UserProfile


class TeamsViewTests(TestCase):
	"""Functional tests for the teams views.

	These tests exercise the public team list/search and the team
	members page. They were added to replace an ad-hoc tmp script and
	provide repeatable checks for the behaviors developers commonly use
	while debugging teams-related UIs.
	"""

	def setUp(self):
		User = get_user_model()
		# create a lead user and a regular member
		self.lead = User.objects.create_user(username='leaduser', password='pass') # type: ignore
		self.member = User.objects.create_user(username='member', password='pass') # type: ignore

		# create a team and assign a lead
		self.team = Team.objects.create(team_name='API Team')
		self.team.lead_user = self.lead
		self.team.save()

		# create profiles and link member to team
		# Profiles provide the canonical team membership used in the UI.
		UserProfile.objects.create(user=self.lead, team=self.team, job_title='Team Lead')
		UserProfile.objects.create(user=self.member, team=self.team, job_title='Engineer')

	def test_team_list_shows_team(self):
		"""The team index should render and include the created team."""
		url = reverse('teams:index')
		self.client.login(username='leaduser', password='pass')
		resp = self.client.get(url, follow=True)
		self.assertEqual(resp.status_code, 200)
		self.assertIn('API Team', resp.content.decode())

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
		# login as member
		self.client.login(username='member', password='pass')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		body = resp.content.decode()
		# member list should include member's username or job title
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
		# Ensure the update appears on dashboard
		dash = reverse('dashboard')
		resp2 = self.client.get(dash)
		self.assertIn('Roadmap', resp2.content.decode())

		# Find the created update id via the DB
		update = TeamUpdate.objects.filter(team=self.team, title='Roadmap').first()
		self.assertIsNotNone(update)

		# Delete it
		url_del = reverse('teams:delete_update', kwargs={'team_id': self.team.pk, 'update_id': update.pk}) # type: ignore
		resp3 = self.client.post(url_del, follow=True)
		self.assertEqual(resp3.status_code, 200)
		# Ensure it's gone
		self.assertFalse(TeamUpdate.objects.filter(pk=update.pk).exists()) # type: ignore

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

# Create your tests here.
