from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class SignUpTests(TestCase):
    def signup(self, **overrides):
        data = {
            "username": "amina",
            "email": "amina@example.com",
            "password1": "Sup3r-secret-pass",
            "password2": "Sup3r-secret-pass",
        }
        data.update(overrides)
        return self.client.post(reverse("signup"), data)

    def test_signup_page_loads(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_creates_user_and_logs_in(self):
        response = self.signup()
        self.assertRedirects(response, reverse("recipes:home"))
        self.assertTrue(User.objects.filter(username="amina", email="amina@example.com").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_passwords_must_match(self):
        response = self.signup(password2="something-else-1")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.exists())

    def test_email_must_be_unique(self):
        User.objects.create_user("existing", email="amina@example.com", password="x")
        response = self.signup()
        self.assertContains(response, "An account with this email already exists.")


class LoginLogoutTests(TestCase):
    def setUp(self):
        User.objects.create_user("amina", password="Sup3r-secret-pass")

    def test_login_with_correct_password(self):
        response = self.client.post(reverse("login"), {"username": "amina", "password": "Sup3r-secret-pass"})
        self.assertRedirects(response, reverse("recipes:home"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_with_wrong_password_fails(self):
        response = self.client.post(reverse("login"), {"username": "amina", "password": "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout(self):
        self.client.login(username="amina", password="Sup3r-secret-pass")
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("recipes:home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_nav_shows_username_when_logged_in(self):
        self.client.login(username="amina", password="Sup3r-secret-pass")
        response = self.client.get(reverse("recipes:home"))
        self.assertContains(response, "Log out (amina)")
