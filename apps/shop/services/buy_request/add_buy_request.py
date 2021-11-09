from authorization.models import User
from shop.dto.buy_request import AddBuyRequestDTO
from shop.models import BuyRequest


class AddBuyRequestService:
    def __init__(self, data: AddBuyRequestDTO):
        self._data = data

    def _get_from_client(self):
        return User.objects.get(id=self._data.from_client_id)

    def _get_car(self):
        return self._data.car

    def execute(self) -> BuyRequest:
        from_client = self._get_from_client()
        car = self._get_car()

        req = BuyRequest.objects.create(
            from_client=from_client,
            car=car,
        )

        return req
