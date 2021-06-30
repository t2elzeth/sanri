from container.models import Container
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


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

    def create(self, validated_data: dict):
        """Create user"""
        confirmPassword = validated_data.pop("confirmPassword")
        if validated_data["password"] != confirmPassword:
            raise ValidationError("Passwords don't match")

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
        cars = user.car_sales_as_owner.all()

        return {
            "number": len(cars),
            "totalAmount": sum(car.total for car in cars),
        }

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
        ]

    def create(self, validated_data: dict):
        """Create user"""
        confirmPassword = validated_data.pop("confirmPassword")
        if validated_data["password"] != confirmPassword:
            raise ValidationError("Passwords don't match")

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

    def create(self, validated_data: dict):
        """Create user"""
        confirmPassword = validated_data.pop("confirmPassword")
        if validated_data["password"] != confirmPassword:
            raise ValidationError("Passwords don't match")

        user = self.Meta.model.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if "username" in validated_data:
            raise ValidationError({"error": "Username cannot be updated!"})
        return super().update(instance, validated_data)
