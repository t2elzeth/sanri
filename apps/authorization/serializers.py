from container.models import Container
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Balance, User


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
        ]
        ref_name = "main"

    def create(self, validated_data: dict):
        """Create user"""
        confirmPassword = validated_data.pop("confirmPassword")
        if validated_data["password"] != confirmPassword:
            raise ValidationError("Passwords don't match")

        validated_data.update({"user_type": User.USER_TYPE_USER})

        user = self.Meta.model.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if "username" in validated_data:
            raise ValidationError({"error": "Username cannot be updated!"})
        return super().update(instance, validated_data)


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

        return {
            "number": len(containers),
            "totalAmount": sum(
                container.totalAmount for container in containers
            ),
        }

    def get_going_to_containers(self, user):
        containers = user.containers.filter(status=Container.STATUS_GOING_TO)

        return {
            "number": len(containers),
            "totalAmount": sum(
                container.totalAmount for container in containers
            ),
        }

    def get_cars_for_sale(self, user):
        cars = user.car_orders.all()

        return {
            "number": len(cars),
            "totalAmount": sum(car.total for car in cars),
        }

    def get_balance_replenishments(self, user):
        balances = user.balances.filter(
            balance_action=Balance.BALANCE_ACTION_REPLENISHMENT
        )

        return {
            "number": len(balances),
            "totalAmount": sum(balance.sum_in_jpy for balance in balances)
        }

    def get_balance_withdrawals(self, user):
        balances = user.balances.filter(
            balance_action=Balance.BALANCE_ACTION_WITHDRAWAL
        )

        return {
            "number": len(balances),
            "totalAmount": sum(balance.sum_in_jpy for balance in balances)
        }

    def get_balance(self, user):
        replenishments = sum(balance.sum_in_jpy for balance in user.balances.filter(
            balance_action=Balance.BALANCE_ACTION_REPLENISHMENT
        ))

        withdrawals = sum(balance.sum_in_jpy for balance in user.balances.filter(
            balance_action=Balance.BALANCE_ACTION_WITHDRAWAL
        ))
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
            'balance'
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

    def update(self, instance, validated_data):
        if "username" in validated_data:
            raise ValidationError({"error": "Username cannot be updated!"})
        return super().update(instance, validated_data)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    auth_token = serializers.CharField(source="key", read_only=True)

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
                self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            return data
        self.fail("invalid_credentials")

    def create(self, validated_data):
        return self.user.login()


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "fullName",
            "username",
            "password",
            "confirmPassword",
            "role",
        ]
        ref_name = "main"

    def create(self, validated_data: dict):
        """Create user"""
        confirmPassword = validated_data.pop("confirmPassword")
        if validated_data["password"] != confirmPassword:
            raise ValidationError("Passwords don't match")

        validated_data.update({"user_type": User.USER_TYPE_EMPLOYEE})

        user = self.Meta.model.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if "username" in validated_data:
            raise ValidationError({"error": "Username cannot be updated!"})
        return super().update(instance, validated_data)


class BalanceSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(source="client",
                                                   write_only=True,
                                                   queryset=User.objects.all())

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
