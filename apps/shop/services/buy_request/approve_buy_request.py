from shop.models import BuyRequest
from shop.dto.buy_request import ApproveBuyRequestDTO


class ApproveBuyRequestService:
    def __init__(self, data: ApproveBuyRequestDTO):
        self._data = data

    def _get_request_instance(self):
        return self._data.request

    def _set_approve_field(self, req: BuyRequest) -> None:
        req.status = BuyRequest.STATUS_APPROVED
        req.save()

    def _decline_other_requests(self, req: BuyRequest):
        BuyRequest.objects.exclude(id=req.id).filter(car__id=req.car.id).update(status=BuyRequest.STATUS_DECLINED)

    def execute(self) -> BuyRequest:
        req = self._get_request_instance()
        self._set_approve_field(req)
        self._decline_other_requests(req)

        return req
