from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework.authtoken.models import Token

from . import managers


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model for authentication"""

    objects = managers.UserManager()

    fullName = models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phoneNumber = models.CharField(max_length=255, blank=True, null=True)
    service = models.CharField(max_length=255, blank=True, null=True)
    atWhatPrice = models.CharField(max_length=255, blank=True, null=True)
    sizeFOB = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=16, unique=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

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


class Balance(models.Model):
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="balances"
    )
    name = models.CharField(max_length=255)
    date = models.DateField()
    sum_in_jpy = models.IntegerField()
    sum_in_usa = models.IntegerField()
    rate = models.IntegerField()

    PAYMENT_TYPE_CASHLESS = "cashless"
    PAYMENT_TYPE_CASH = "cash"
    PAYMENT_TYPE_CHOICES = (
        (PAYMENT_TYPE_CASHLESS, PAYMENT_TYPE_CASHLESS),
        (PAYMENT_TYPE_CASH, PAYMENT_TYPE_CASH),
    )
    payment_type = models.CharField(
        max_length=255, choices=PAYMENT_TYPE_CHOICES
    )
    sender_name = models.CharField(max_length=255)
    comment = models.TextField()

    BALANCE_ACTION_REPLENISHMENT = "replenishment"
    BALANCE_ACTION_WITHDRAWAL = "withdrawal"
    BALANCE_ACTION_CHOICES = (
        (BALANCE_ACTION_REPLENISHMENT, BALANCE_ACTION_REPLENISHMENT),
        (BALANCE_ACTION_WITHDRAWAL, BALANCE_ACTION_WITHDRAWAL),
    )
    balance_action = models.CharField(
        max_length=255, choices=BALANCE_ACTION_CHOICES
    )

    def __str__(self):
        return f"{self.name}: {self.sum_in_usa}: {self.balance_action}"
