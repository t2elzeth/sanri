from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..models import Token, User
from .mixins import CreateUserAndSuperuserAndSetCredentialsMixin, UserDataMixin


class TestUserSignUp(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("user-signup")
        self.valid_payload = UserDataMixin.USER_DATA

    def test_signup_using_valid_payload(self):
        """Test trying to signup using valid data case"""
        response = self.client.post(self.url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_using_empty_payload(self):
        """Test trying to signup using empty data case"""
        response = self.client.post(self.url, {})

        self.assertIn("username", response.data)
        self.assertIn("password", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_already_exists(self):
        """Test user already exists case"""
        User.objects.create_user(**self.valid_payload)

        response = self.client.post(self.url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestLogin(CreateUserAndSuperuserAndSetCredentialsMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("token-auth-login")
        self.valid_credentials = self.SUPERUSER_DATA
        self.invalid_credentials = {
            "username": "invalidcredentials",
            "password": "invalidcredentialspassword",
        }

    def test_login_with_valid_credentials(self):
        """Test login"""
        response = self.client.post(self.url, self.SUPERUSER_DATA)

        self.assertTrue(Token.objects.filter(user=self.superuser).exists())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(
            "auth_token",
            response.data,
            "auth_token is not present in response.data",
        )

    def test_login_with_invalid_credentials(self):
        """Test trying to login using invalid credentials"""
        response = self.client.post(self.url, self.invalid_credentials)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("auth_token", response.data)


class TestLogout(CreateUserAndSuperuserAndSetCredentialsMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("token-auth-logout")

    def test_logout(self):
        """Test user logout"""
        self.set_credentials()

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Token.objects.filter(user=self.superuser).exists(),
            "Token was not deleted after logout",
        )

    def test_logout_without_credentials(self):
        """Test logout without providing auth credentials"""
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
