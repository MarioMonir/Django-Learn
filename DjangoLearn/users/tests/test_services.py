from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed

from DjangoLearn.users.services import generate_tokens, login_user, logout_user, register_user

User = get_user_model()


class RegisterUserServiceTest(TestCase):
    def setUp(self):
        self.payload = {
            "email": "mario@test.com",
            "password": "testpass123",
            "first_name": "Mario",
            "last_name": "Monir",
        }

    def test_register_returns_tokens(self):
        result = register_user(self.payload)
        self.assertIn("access", result)
        self.assertIn("refresh", result)

    def test_register_creates_user(self):
        register_user(self.payload)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.email, self.payload["email"])

    def test_register_hashes_password(self):
        register_user(self.payload)
        user = User.objects.first()
        self.assertNotEqual(user.password, self.payload["password"])
        self.assertTrue(user.check_password(self.payload["password"]))

    def test_register_duplicate_email_fails(self):
        register_user(self.payload)
        with self.assertRaises(Exception):
            register_user(self.payload)


class LoginUserServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="mario@test.com",
            password="testpass123",
            first_name="Mario",
            last_name="Monir",
        )

    def test_login_returns_tokens(self):
        result = login_user("mario@test.com", "testpass123")
        self.assertIn("access", result)
        self.assertIn("refresh", result)

    def test_login_wrong_password_fails(self):
        with self.assertRaises(AuthenticationFailed):
            login_user("mario@test.com", "wrongpassword")

    def test_login_wrong_email_fails(self):
        with self.assertRaises(AuthenticationFailed):
            login_user("wrong@test.com", "testpass123")


class LogoutUserServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="mario@test.com",
            password="testpass123",
            first_name="Mario",
            last_name="Monir",
        )

    def test_logout_blacklists_token(self):
        tokens = generate_tokens(self.user)
        logout_user(tokens["refresh"])
        with self.assertRaises(Exception):
            logout_user(tokens["refresh"])
