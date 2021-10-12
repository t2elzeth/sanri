import factory

from authorization.models import User


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    fullName = factory.Faker("name")
    country = "KG"
    email = "client@gmail.com"
    phoneNumber = factory.Faker("phone_number")

    service = User.SERVICE_ENTIRE
    atWhatPrice = User.AT_WHAT_PRICE_BY_FACT
    sizeFOB = factory.Faker("pyint", min_value=1, max_value=200_000)
    username = factory.Faker("user_name")
    user_type = User.USER_TYPE_CLIENT
