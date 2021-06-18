from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserDataMixin:
    USER_DATA = {
        "username": "testuser",
        "password": "admin",
    }
    SUPERUSER_DATA = {
        "username": "testsuperuser",
        "password": "admin",
    }


class CreateUserAndSuperuserMixin(UserDataMixin):
    def setUp(self):
        self.user = User.objects.create_user(**self.USER_DATA)
        self.superuser = User.objects.create_superuser(**self.SUPERUSER_DATA)
        self.supertoken = Token.objects.create(user=self.superuser)


class CreateUserAndSuperuserAndSetCredentialsMixin(
    CreateUserAndSuperuserMixin
):
    AUTHENTICATION_CREDENTIALS = "Token {}"

    def set_credentials(self, token=None):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.AUTHENTICATION_CREDENTIALS.format(
                self.supertoken.key if token is None else token.key
            )
        )
