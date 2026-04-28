from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse

from organizations.models import Department
from .models import UserProfile


class AccountsViewTests(TestCase):
	"""Tests for signup, login, logout, and profile pages."""

	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(username="jane", password="pass12345", email="jane@example.com")  # type: ignore[attr-defined]
		self.admin = User.objects.create_user(  # type: ignore[attr-defined]
			username="adminuser",
			password="pass12345",
			email="admin@example.com",
			is_staff=True,
		)
		self.department = Department.objects.create(dept_name="Engineering", head_user="Director")
		self.profile = UserProfile.objects.create(user=self.user, department=self.department, job_title="Engineer")

	@patch("accounts.views.send_mail")
	def test_signup_creates_user_and_redirects_to_login(self, mock_send_mail):
		"""Signup should create the user and send the welcome email hook."""
		url = reverse("accounts:signup")
		response = self.client.post(
			url,
			{
				"username": "newuser",
				"first_name": "New",
				"last_name": "User",
				"email": "newuser@example.com",
				"password1": "ComplexPass123!",
				"password2": "ComplexPass123!",
			},
			follow=True,
		)

		self.assertEqual(response.status_code, 200)
		self.assertTrue(get_user_model().objects.filter(username="newuser").exists())
		mock_send_mail.assert_called_once()

	def test_login_redirects_authenticated_user_to_dashboard(self):
		"""Valid credentials should log the user in and redirect them home."""
		url = reverse("accounts:login")
		response = self.client.post(url, {"username": "jane", "password": "pass12345"}, follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertGreaterEqual(len(response.redirect_chain), 1)
		self.assertEqual(response.redirect_chain[0][0], "/")
		self.assertIn(SESSION_KEY, self.client.session)

	def test_logout_clears_session_and_redirects(self):
		"""Logout should end the session and send the user back to login."""
		self.client.login(username="jane", password="pass12345")
		url = reverse("accounts:logout")
		response = self.client.get(url)

		self.assertEqual(response.status_code, 302)
		self.assertNotIn(SESSION_KEY, self.client.session)
		self.assertEqual(response["Location"], "/accounts/login/")

	def test_profile_page_creates_profile_and_renders(self):
		"""The profile page should load for the logged-in user."""
		self.client.login(username="jane", password="pass12345")
		url = reverse("accounts:profile")
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["profile_obj"].pk, self.profile.pk)
		self.assertEqual(response.context["user"].username, "jane")

	def test_user_access_denies_non_admin(self):
		"""Regular users should be sent away from the admin access page."""
		self.client.login(username="jane", password="pass12345")
		url = reverse("accounts:user_access")
		response = self.client.get(url, follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertGreaterEqual(len(response.redirect_chain), 1)
		self.assertEqual(response.redirect_chain[0][0], "/")

	def test_user_access_shows_users_for_admin(self):
		"""Staff users should see the user management page."""
		self.client.login(username="adminuser", password="pass12345")
		url = reverse("accounts:user_access")
		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)
		body = response.content.decode()
		self.assertIn("jane", body)
		self.assertIn("adminuser", body)
