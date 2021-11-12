from shop.models import BuyRequest
from shop.dto.buy_request import DeclineBuyRequestDTO


class DeclineBuyRequestService:
    def __init__(self, data: DeclineBuyRequestDTO):
        self._data = data

    def _get_request_instance(self):
        return self._data.request

    def _set_approved_field(self, req: BuyRequest) -> None:
        req.status = BuyRequest.STATUS_DECLINED
        req.save()

    def execute(self) -> BuyRequest:
        req = self._get_request_instance()
        self._set_approved_field(req)

        return req
