from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountAuthenticationTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("accounts:dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("accounts:login") + "?next=" + reverse("accounts:dashboard"))

    def test_home_urls_are_available_from_the_namespace(self):
        self.assertEqual(reverse("home:home"), "/")
        self.assertEqual(reverse("home:information-centre"), "/information-centre/")

    def test_information_centre_page_renders(self):
        response = self.client.get(reverse("home:information-centre"))

        self.assertEqual(response.status_code, 200)

    def test_user_can_register_and_reach_dashboard(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:dashboard"))

        dashboard_response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(dashboard_response.status_code, 200)
