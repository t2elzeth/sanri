from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token

from . import managers, model_helpers


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
    AT_WHAT_PRICE_BY_FOB2 = "by_fob2"
    AT_WHAT_PRICE_CHOICES = (
        (AT_WHAT_PRICE_BY_FACT, AT_WHAT_PRICE_BY_FACT),
        (AT_WHAT_PRICE_BY_FOB, AT_WHAT_PRICE_BY_FOB),
        (AT_WHAT_PRICE_BY_FOB2, AT_WHAT_PRICE_BY_FOB2),
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
    transportation_limit = models.IntegerField(default=6000)

    USER_TYPE_SUPERUSER = "superuser"
    USER_TYPE_ADMIN = "admin"
    USER_TYPE_SALES_MANAGER = "sales_manager"
    USER_TYPE_YARD_MANAGER = "yard_manager"
    USER_TYPE_CLIENT = "client"
    USER_TYPE_EMPLOYEE = "employee"
    USER_TYPE_CHOICES = (
        (USER_TYPE_SUPERUSER, USER_TYPE_SUPERUSER),
        (USER_TYPE_ADMIN, USER_TYPE_ADMIN),
        (USER_TYPE_SALES_MANAGER, USER_TYPE_SALES_MANAGER),
        (USER_TYPE_YARD_MANAGER, USER_TYPE_YARD_MANAGER),
        (USER_TYPE_CLIENT, USER_TYPE_CLIENT),
        (USER_TYPE_EMPLOYEE, USER_TYPE_EMPLOYEE),
    )
    user_type = models.CharField(
        max_length=255, choices=USER_TYPE_CHOICES, default=USER_TYPE_SUPERUSER
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"Account of {self.get_username()}"

    @property
    def balance(self) -> model_helpers.UserBalance:
        return model_helpers.UserBalance(self)

    @property
    def works_by(self) -> model_helpers.UserWorksBy:
        return model_helpers.UserWorksBy(self)

    def login(self):
        token, _ = Token.objects.get_or_create(user=self)
        return token

    def logout(self):
        Token.objects.filter(user=self).delete()

    class Meta:
        ordering = ("id",)

    def save(self, *args, **kwargs):
        if self.id is not None:
            previous = User.objects.get(id=self.id)

            if self.transportation_limit != previous.transportation_limit:
                for order in self.car_orders.all():
                    order.save()

        if self.works_by.by_fact:
            self.sizeFOB = 0

        return super().save(*args, **kwargs)


class Balance(models.Model):
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="balances"
    )
    date = models.DateField(default=timezone.now)
    sum_in_jpy = models.IntegerField()
    sum_in_usa = models.IntegerField(default=0)
    rate = models.DecimalField(default=0, decimal_places=2, max_digits=10)

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
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.client.fullName}: {self.sum_in_usa}: {self.balance_action}"
        )

    class Meta:
        ordering = ("id",)


class ManagedUser(models.Model):
    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="managed_users_as_manager"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="managed_users_as_user"
    )

    class Meta:
        ordering = ("id",)
