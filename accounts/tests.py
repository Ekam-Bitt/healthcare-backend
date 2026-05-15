from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterViewTests(APITestCase):
    """Tests for the user registration endpoint."""

    url = "/api/auth/register/"

    def test_register_success(self):
        """Registration with valid data returns 201 and JWT tokens."""
        data = {"name": "Test User", "email": "test@example.com", "password": "securepass123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tokens", response.data)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_register_missing_password(self):
        """Registration without password returns 400."""
        data = {"name": "Test", "email": "test@example.com"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        """Registration with an already-used email returns 400."""
        data = {"name": "User 1", "email": "dup@example.com", "password": "securepass123"}
        self.client.post(self.url, data)
        response = self.client.post(self.url, {**data, "name": "User 2"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_password(self):
        """Password shorter than 8 characters is rejected."""
        data = {"name": "Test", "email": "test@example.com", "password": "short"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(APITestCase):
    """Tests for the login (token obtain) endpoint."""

    url = "/api/auth/login/"

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="securepass123")

    def test_login_success(self):
        """Login with valid credentials returns JWT tokens."""
        data = {"username": "testuser", "password": "securepass123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password(self):
        """Login with wrong password returns 401."""
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
