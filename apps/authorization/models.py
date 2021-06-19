from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework.authtoken.models import Token

from . import managers


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model for authentication"""

    objects = managers.UserManager()

    fullName = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phoneNumber = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    atWhatPrice = models.CharField(max_length=255)
    sizeFOB = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"Account of {self.get_username()}"

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.logout()
        self.is_active = False
        self.save()

    def login(self):
        token, _ = Token.objects.get_or_create(user=self)
        return token

    def logout(self):
        Token.objects.filter(user=self).delete()
