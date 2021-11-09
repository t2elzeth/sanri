from container.models import Container, ContainerCar
from django.contrib.auth import authenticate
from income.models import Income
from rest_framework import serializers
from rest_framework.exceptions import (
    APIException,
    NotAuthenticated,
    ValidationError,
)

from .models import Balance, ManagedUser, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "fullName",
            "country",
            "email",
            "phoneNumber",
            "service",
            "atWhatPrice",
            "sizeFOB",
            "username",
            "password",
            "confirmPassword",
            "createdAt",
            "user_type",
        ]
        ref_name = "main"

    def create(self, validated_data: dict):
        """Create user"""
        confirmPassword = validated_data.pop("confirmPassword")
        if validated_data["password"] != confirmPassword:
            raise ValidationError("Passwords don't match")

        validated_data.update(
            {
                "user_type": validated_data.pop(
                    "user_type", User.USER_TYPE_EMPLOYEE
                )
            }
        )

        user = self.Meta.model.objects.create_user(**validated_data)
        return user


class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)
    shipped_containers = serializers.SerializerMethodField(read_only=True)
    going_to_containers = serializers.SerializerMethodField(read_only=True)
    cars_for_sale = serializers.SerializerMethodField(read_only=True)
    balance_replenishments = serializers.SerializerMethodField(read_only=True)
    balance_withdrawals = serializers.SerializerMethodField(read_only=True)
    balance = serializers.SerializerMethodField(read_only=True)

    def get_shipped_containers(self, user):
        containers = user.containers.filter(status=Container.STATUS_SHIPPED)
        total = 0
        for container in containers:
            container_total = 0
            cars_total = sum(
                container_car.car.get_total()
                for container_car in container.container_cars.all()
            )
            if user.atWhatPrice == User.AT_WHAT_PRICE_BY_FACT:
                container_total = (
                    cars_total
                    + container.commission
                    + container.containerTransportation
                    + container.packagingMaterials
                    + container.wheel_recycling.sum
                    - container.wheel_sales.sum
                )
            elif user.atWhatPrice == User.AT_WHAT_PRICE_BY_FOB:
                container_total = cars_total + container.loading
            elif user.atWhatPrice == User.AT_WHAT_PRICE_BY_FOB2:
                container_total = cars_total + container.transportation
            total += container_total
        return {
            "number": len(containers),
            "totalAmount": total,
        }

    def get_going_to_containers(self, user):
        containers = user.containers.filter(status=Container.STATUS_GOING_TO)

        total = 0
        for container in containers:
            container_total = 0
            cars_total = sum(
                container_car.car.get_total()
                for container_car in container.container_cars.all()
            )
            if user.atWhatPrice == User.AT_WHAT_PRICE_BY_FACT:
                container_total = (
                    cars_total
                    + container.commission
                    + container.containerTransportation
                    + container.packagingMaterials
                    + container.wheel_recycling.sum
                    - container.wheel_sales.sum
                )
            elif user.atWhatPrice == User.AT_WHAT_PRICE_BY_FOB:
                container_total = cars_total + container.loading
            elif user.atWhatPrice == User.AT_WHAT_PRICE_BY_FOB2:
                container_total = cars_total + container.transportation
            total += container_total

        return {"number": len(containers), "totalAmount": total}

    def get_cars_for_sale(self, user):
        car_ids = list(
            [
                el["car__id"]
                for el in ContainerCar.objects.all().values("car__id")
            ]
        )
        cars = user.car_orders.exclude(id__in=car_ids)

        total_key = {
            User.AT_WHAT_PRICE_BY_FACT: "total",
            User.AT_WHAT_PRICE_BY_FOB: "total_FOB",
            User.AT_WHAT_PRICE_BY_FOB2: "total_FOB2",
        }

        key = total_key[user.atWhatPrice]

        return {
            "number": len(cars),
            "totalAmount": sum(getattr(car, key) for car in cars),
        }

    def get_balance_replenishments(self, user):
        balances = user.balances.filter(
            balance_action=Balance.BALANCE_ACTION_REPLENISHMENT
        )

        return {
            "number": len(balances),
            "totalAmount": sum(balance.sum_in_jpy for balance in balances),
        }

    def get_balance_withdrawals(self, user):
        balances = user.balances.filter(
            balance_action=Balance.BALANCE_ACTION_WITHDRAWAL
        )

        return {
            "number": len(balances),
            "totalAmount": sum(balance.sum_in_jpy for balance in balances),
        }

    def get_balance(self, user):
        replenishments = sum(
            balance.sum_in_jpy
            for balance in user.balances.filter(
                balance_action=Balance.BALANCE_ACTION_REPLENISHMENT
            )
        )

        withdrawals = sum(
            balance.sum_in_jpy
            for balance in user.balances.filter(
                balance_action=Balance.BALANCE_ACTION_WITHDRAWAL
            )
        )

        if user.username == "sanrijp":
            replenishments += sum(
                income.amount for income in Income.objects.all()
            )

        return replenishments - withdrawals

    class Meta:
        model = User
        fields = [
            "id",
            "fullName",
            "country",
            "email",
            "phoneNumber",
            "service",
            "atWhatPrice",
            "sizeFOB",
            "username",
            "password",
            "confirmPassword",
            "createdAt",
            "shipped_containers",
            "going_to_containers",
            "cars_for_sale",
            "balance_replenishments",
            "balance_withdrawals",
            "balance",
        ]
        ref_name = "main"

    def create(self, validated_data: dict):
        """Create user"""
        confirmPassword = validated_data.pop("confirmPassword")
        if validated_data["password"] != confirmPassword:
            raise ValidationError("Passwords don't match")

        validated_data.update({"user_type": User.USER_TYPE_CLIENT})

        user = self.Meta.model.objects.create_user(**validated_data)
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    auth_token = serializers.CharField(source="key", read_only=True)
    user_type = serializers.CharField(source="user.user_type", read_only=True)
    user = UserSerializer(read_only=True)

    default_error_messages = {
        "invalid_credentials": "Unable to log in with provided credentials.",
        "inactive_account": "User account is disabled.",
    }

    def validate(self, data):
        password = data.get("password")
        params = {"username": data.get("username")}
        self.user = authenticate(
            request=self.context.get("request"), password=password, **params
        )
        if not self.user:
            self.user = User.objects.get_object_or_none(**params)
            if self.user and not self.user.check_password(password):
                # self.fail("invalid_credentials")
                # raise ValidationError(self.default_error_messages['invalid_credentials'])
                raise NotAuthenticated(
                    self.default_error_messages["invalid_credentials"]
                )
        if self.user and self.user.is_active:
            return data
        self.fail("invalid_credentials")

    def create(self, validated_data):
        return self.user.login()


class BalanceSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        source="client", write_only=True, queryset=User.objects.all()
    )

    class Meta:
        model = Balance
        fields = [
            "id",
            "client",
            "client_id",
            "date",
            "sum_in_jpy",
            "sum_in_usa",
            "rate",
            "payment_type",
            "sender_name",
            "comment",
            "balance_action",
        ]
        ref_name = "main"


class ManagedUserSerializer(serializers.ModelSerializer):
    user = ClientSerializer()

    class Meta:
        model = ManagedUser
        fields = ["user"]


class ManagerSerializer(UserSerializer):
    managed_users_ids = serializers.ListSerializer(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    managed_users = ManagedUserSerializer(
        source="managed_users_as_manager", read_only=True, many=True
    )

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            "managed_users_ids",
            "managed_users",
        ]

    def create(self, validated_data: dict):
        print(validated_data)
        managed_user_ids = validated_data.pop("managed_users_ids", [])
        print(managed_user_ids)
        manager = super().create(validated_data)
        for user_id in managed_user_ids:
            manager.managed_users_as_manager.create(
                user=User.objects.get(id=user_id)
            )

        return manager

    def update(self, instance, validated_data):
        managed_user_ids = validated_data.pop("managed_users_ids", [])

        manager = super().update(instance, validated_data)

        manager.managed_users_as_manager.all().delete()
        for user_id in managed_user_ids:
            manager.managed_users_as_manager.create(
                user=User.objects.get(id=user_id)
            )

        return manager
