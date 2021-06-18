from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)
    login = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = [
            'fullName',
            'country',
            'email',
            'phoneNumber',
            'service',
            'atWhatPrice',
            'sizeFOB',
            'login',
            'password',
            'confirmPassword'
        ]

    def create(self, validated_data: dict):
        """Create user"""
        if validated_data['password'] != validated_data['confirmPassword']:
            raise ValidationError("Passwords don't match")

        user = self.Meta.model.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if "login" in validated_data:
            raise ValidationError({"error": "Login cannot be updated!"})
        return super().update(instance, validated_data)


class TokenSerializer(serializers.Serializer):
    login = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    auth_token = serializers.CharField(source="key", read_only=True)

    default_error_messages = {
        "invalid_credentials": "Unable to log in with provided credentials.",
        "inactive_account": "User account is disabled.",
    }

    def validate(self, data):
        password = data.get("password")
        params = {"username": data.get("login")}
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
