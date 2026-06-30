from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from DjangoLearn.users.services import generate_tokens

User = get_user_model()


class RegisterViewTest(APITestCase):
    def setUp(self):
        self.payload = {
            "email": "mario@test.com",
            "password": "testpass123",
            "first_name": "Mario",
            "last_name": "Monir",
        }

    def test_register_returns_201(self):
        response = self.client.post(reverse("register"), data=self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_register_missing_email_returns_400(self):
        self.payload.pop("email")
        response = self.client.post(reverse("register"), data=self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_password_returns_400(self):
        self.payload.pop("password")
        response = self.client.post(reverse("register"), data=self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email_returns_400(self):
        self.client.post(reverse("register"), data=self.payload, format="json")
        response = self.client.post(reverse("register"), data=self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="mario@test.com",
            password="testpass123",
            first_name="Mario",
            last_name="Monir",
        )

    def test_login_returns_200(self):
        response = self.client.post(reverse("login"), data={
            "email": "mario@test.com",
            "password": "testpass123",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password_returns_401(self):
        response = self.client.post(reverse("login"), data={
            "email": "mario@test.com",
            "password": "wrongpassword",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_wrong_email_returns_403(self):
        response = self.client.post(reverse("login"), data={
            "email": "wrong@test.com",
            "password": "testpass123",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LogoutViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="mario@test.com",
            password="testpass123",
            first_name="Mario",
            last_name="Monir",
        )
        tokens = generate_tokens(self.user)
        self.access = tokens["access"]
        self.refresh = tokens["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_logout_returns_204(self):
        response = self.client.post(reverse("logout"), data={"refresh": self.refresh}, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_without_token_returns_401(self):
        self.client.credentials()
        response = self.client.post(reverse("logout"), data={"refresh": self.refresh}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MeViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="mario@test.com",
            password="testpass123",
            first_name="Mario",
            last_name="Monir",
        )
        tokens = generate_tokens(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

    def test_me_returns_200(self):
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["first_name"], self.user.first_name)

    def test_me_without_token_returns_401(self):
        self.client.credentials()
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
