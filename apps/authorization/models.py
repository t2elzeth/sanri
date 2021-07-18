from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework.authtoken.models import Token
from django.utils import timezone
from . import managers


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model for authentication"""

    objects = managers.UserManager()

    fullName = models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phoneNumber = models.CharField(max_length=255, blank=True, null=True)

    SERVICE_DISSECTION = "dissection"
    SERVICE_ENTIRE = "entire"
    SERVICE_CHOICES = (
        (SERVICE_DISSECTION, SERVICE_DISSECTION),
        (SERVICE_ENTIRE, SERVICE_ENTIRE),
    )
    service = models.CharField(
        max_length=255, choices=SERVICE_CHOICES, default=SERVICE_ENTIRE
    )

    AT_WHAT_PRICE_BY_FACT = "by_fact"
    AT_WHAT_PRICE_BY_FOB = "by_fob"
    AT_WHAT_PRICE_CHOICES = (
        (AT_WHAT_PRICE_BY_FACT, AT_WHAT_PRICE_BY_FACT),
        (AT_WHAT_PRICE_BY_FOB, AT_WHAT_PRICE_BY_FOB),
    )
    atWhatPrice = models.CharField(
        max_length=255,
        choices=AT_WHAT_PRICE_CHOICES,
        default=AT_WHAT_PRICE_BY_FACT,
    )
    sizeFOB = models.IntegerField(default=0)
    username = models.CharField(max_length=16, unique=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    USER_TYPE_USER = "user"
    USER_TYPE_CLIENT = "client"
    USER_TYPE_EMPLOYEE = "employee"
    USER_TYPE_CHOICES = (
        (USER_TYPE_USER, USER_TYPE_USER),
        (USER_TYPE_CLIENT, USER_TYPE_CLIENT),
        (USER_TYPE_EMPLOYEE, USER_TYPE_EMPLOYEE),
    )
    user_type = models.CharField(
        max_length=255, choices=USER_TYPE_CHOICES, default=USER_TYPE_USER
    )

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
    date = models.DateField(default=timezone.now)
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.client.fullName}: {self.sum_in_usa}: {self.balance_action}"
        )
