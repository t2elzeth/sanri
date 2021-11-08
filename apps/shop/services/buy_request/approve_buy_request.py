from shop.models import BuyRequest
from shop.dto.buy_request import ApproveBuyRequestDTO


class ApproveBuyRequestService:
    def __init__(self, data: ApproveBuyRequestDTO):
        self._data = data

    def _get_request_instance(self):
        return BuyRequest.objects.get(id=self._data.request_id)

    def _set_approve_field(self, req: BuyRequest) -> None:
        req.approved = True
        req.save()

    def execute(self) -> BuyRequest:
        req = self._get_request_instance()
        self._set_approve_field(req)

        return req
