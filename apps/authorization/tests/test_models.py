from django.test import TestCase

from ..models import Token, User
from .mixins import CreateUserAndSuperuserMixin, UserDataMixin


class UserModelTests(UserDataMixin, TestCase):
    def test_user_creation(self):
        """Test creation of user"""
        user = User.objects.create_user(**self.USER_DATA)

        self.assertEqual(user.id, 1)
        self.assertFalse(user.is_active, "User is not deactivated by default")
        self.assertFalse(
            user.is_staff, "Common user mustn't be staff by default"
        )
        self.assertFalse(
            user.is_superuser, "Common user mustn't be superuser by default"
        )
        self.assertTrue(user.check_password(self.USER_DATA["password"]))
        self.assertEqual(user.get_username(), self.USER_DATA["username"])

    def test_super_user_creation(self):
        """Test creation of superuser"""
        superuser = User.objects.create_superuser(**self.USER_DATA)

        self.assertTrue(
            superuser.is_active, "Superuser is not active by default"
        )
        self.assertTrue(
            superuser.is_superuser, "Superuser's `is_superuser` is not True"
        )
        self.assertTrue(
            superuser.is_staff, "Superuser's `is_staff` is not True"
        )
        self.assertIsInstance(superuser, User)


class TestUserActivateMethod(CreateUserAndSuperuserMixin, TestCase):
    def test_user_activate_method(self):
        """
        Test
        >>> user.activate()
        """
        self.user.activate()

        self.assertTrue(self.user.is_active)


class TestUserDeactivateMethod(CreateUserAndSuperuserMixin, TestCase):
    def test_user_deactivate_method(self):
        """
        Test
        >>> user.deactivate()
        """
        self.superuser.deactivate()

        self.assertFalse(self.superuser.is_active)
        self.assertFalse(Token.objects.filter(user=self.superuser).exists())
