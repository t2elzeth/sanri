from rest_framework.authtoken.models import Token

from authorization.models import User


class Authenticate:
    AUTHENTICATION_CREDENTIALS = "Token {}"

    def set_credentials(self, token: Token) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=self.AUTHENTICATION_CREDENTIALS.format(
                token.key
            )
        )

    def create_token(self, user: User) -> Token:
        token, created = Token.objects.get_or_create(user=user)
        return token
